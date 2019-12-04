## Ported by OSOP, Volcan, Panama June, 2012: http://www.osop.com.pa
##
##
## OSOP Programmer: Stacey Anne Rieck (stace.rieck@gmail.com)
## OSOP Project Director: Branden Carl Christensen (branden.christensen@osop.com.pa)
##
##
## Original MATLAB scripts:
## plot_z_surface.m by David Dorran (david.dorran@dit.ie) [2011]
## zpgui.m Author: Tom Krauss (9/1/98); Adapted by: David Dorran [2011]
## For original MATLAB scripts see: http://dadorran.wordpress.com/2012/04/07/zpgui/
##

from pylab import *
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy
from scipy import signal
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams
from matplotlib import colors
from matplotlib.widgets import CheckButtons

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import polelist
import zerolist
import rangefreq
import addgain
import deletepole as delp
from sympy.abc import Z

## EDITABLE VALUES-----------------------------
## Surface resolution between 0.02 and 0.1
## 0.02 is a very high resolution plot (very slow)
## 0.1 is a very low resolution plot (fast)
## Default value is 0.05
## DISCLAIMER: Choosing numbers outside of this range could result in unusual/unexpected behavior. Use at your own risk.
surface_resolution = 1
##---------------------------------------------

plt.ioff()
z = [0, 0]
p = [0, 0]
zh = []
ph = []
ax = [0, 0, 0]
plabels = [0, 0]
zlabels = [0, 0]
thisline = None
polecount = 0;
zerocount = 0;
surface_toggle = 1;
disable_3d_global = True;
version = 3.70
highres = False

fs = 100
G = 2.99e8;
Xmin = 0;
Xmax = 100;
fig2_closed = False;
warnings.simplefilter("ignore", ComplexWarning)


def recompute(self=None, event=None):
    global axfig2, disable_3d_global, freq, fig, fig2
    global z, p, freq, surf

    axes(ax[0])
    zplane(ax[0]);
    plotfilterchar();

    if (disable_3d_global == False):
        plot_z_surface(p, z, axfig2)
        fig2.canvas.draw();

    fig.canvas.draw();


def recompute_only_fig1(self=None, event=None):
    global ax, disable_3d_global, freq, fig, fig2
    global z, p, freq, surf

    plotfilterchar();

    fig.canvas.draw();


def zplane(ax):
    global maxval;
    uc = patches.Circle((0, 0), radius=1, fill=False, color='black', ls='dashed')
    ax.add_patch(uc)

    combine = p + z
    absval = numpy.abs(combine)
    maxval = 0;
    if (combine != []):
        for i, val in enumerate(absval):
            if (val >= maxval):
                maxval = val
                pos = i
        if (numpy.abs(combine[pos].real) > numpy.abs(combine[pos].imag)):
            maxval = combine[pos].real
        else:
            maxval = combine[pos].imag
    else:
        maxval = 0.5

    # set the ticks
    r = 1.5;
    plt.axis('scaled');
    plt.axis([-r, r, -r, r])
    ticks = [-2 * maxval, -maxval, 0, maxval, 2 * maxval];
    plt.xticks(ticks);
    plt.yticks(ticks)
    plt.xlabel('Real Part')
    plt.ylabel('Imaginary Part')
    plt.grid(b=True, which='major', axis='both');

    return ax


def plot_z_surface(pole_positions_orig, zero_positions_orig, ax, CameraPos=None, CameraUpVec=None,
                   surface_display_opts=None):
    global surf, surface_resolution, z_grid, X, Y, fig2, maxval;

    i_decimal = 0;
    temp_val = int(abs(maxval))
    flag = 0;
    if (temp_val > 100):
        while (temp_val >= 1):
            temp_val = temp_val / 10;
            i_decimal = i_decimal + 1;
        surface_resolution = 1;
        surface_limit = int(round(abs(maxval + maxval / 2), -(i_decimal - 1)))
    else:

        if (temp_val <= 1):
            surface_resolution = 0.08;
            surface_limit = 1.7;
        if (temp_val > 1) and (temp_val <= 20):
            surface_resolution = 0.8;
            surface_limit = 27;
        if (temp_val > 20) and (temp_val <= 40):
            surface_resolution = 1.5;
            surface_limit = 47
        if (temp_val > 40) and (temp_val <= 60):
            surface_resolution = 3;
            surface_limit = 67
        if (temp_val > 60):
            surface_resolution = 5;
            surface_limit = 100

    while ((i_decimal - 2) > 0):
        surface_resolution = surface_resolution * 10
        i_decimal = i_decimal - 1;
    # print surface_resolution
    # print surface_limit
    min_val = -surface_limit;
    max_val = surface_limit;
    if (max_val > 150) and (max_val <= 1000):
        surface_resolution = surface_resolution * 5
    # print surface_resolution
    ax = fig2.add_subplot(111, projection='3d')

    X = numpy.arange(min_val, max_val, surface_resolution)
    Y = numpy.arange(min_val, max_val, surface_resolution)
    X, Y = numpy.meshgrid(X, Y)

    z_grid = X + Y * 1j;
    z_surface = z_grid * 0;

    pole_positions = numpy.round(pole_positions_orig, 1) + surface_resolution / 2 + (surface_resolution / 2) * 1j;
    zero_positions = numpy.round(zero_positions_orig, 1) + surface_resolution / 2 + (surface_resolution / 2) * 1j;

    for k in range(0, len(zero_positions)):
        if (zero_positions_orig[k].imag == 0):
            z_surface = z_surface + 20 * log10((z_grid - zero_positions[k]));
        else:
            z_surface = z_surface + 20 * log10((z_grid - zero_positions[k].real - zero_positions[k].imag * 1j));
            z_surface = z_surface + 20 * log10((z_grid - zero_positions[k].real + zero_positions[k].imag * 1j));

    for k in range(0, len(pole_positions)):
        if (pole_positions_orig[k].imag == 0):
            z_surface = z_surface - 20 * log10((z_grid - pole_positions[k]));
        else:
            z_surface = z_surface - 20 * log10((z_grid - pole_positions[k].real - pole_positions[k].imag * 1j));
            z_surface = z_surface - 20 * log10((z_grid - pole_positions[k].real + pole_positions[k].imag * 1j));

    mag_arr = []

    for iz, iz_val in enumerate(z_surface):
        for jz, jz_val in enumerate(z_surface[iz]):
            mag_arr.append((z_surface[iz][jz]).real)

    z_max = max(mag_arr);
    z_min = min(mag_arr);

    cmap = cm.jet
    lev = numpy.arange(z_min, z_max + surface_resolution / 2, 1);
    norml = colors.BoundaryNorm(lev, 256)

    # Zm = ma.masked_where((abs(z_grid) < 1.02) & (abs(z_grid) > 0.98), (z_surface))
    # z_surface[where(ma.getmask(Zm)==True)] = numpy.nan

    if (surface_toggle == 1):
        surf = ax.plot_surface(X, Y, z_surface, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True,
                               norm=norml)


    else:
        surf = ax.plot_wireframe(X, Y, z_surface, rstride=1, cstride=1)

    ticks = [-surface_limit / 2, surface_limit / 2];

    ax.set_xticks(ticks);
    ax.set_yticks(ticks);
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_zlabel('Mag(db)', ha='left')
    plt.setp(ax.get_zticklabels(), fontsize=7)
    plt.setp(ax.get_xticklabels(), fontsize=7)
    plt.setp(ax.get_yticklabels(), fontsize=7)

    ax.grid(b=None);


def plotfilterchar():
    global z, p, freq, ax, G

    b = [1]
    a = [1]

    axes(ax[1])
    plt.cla();
    z_arr = numpy.array(z)
    p_arr = numpy.array(p)
    # print len(p_arr)
    b, a = signal.zpk2tf(z_arr, p_arr, 1)

    Nfft = 256;
    w, h = signal.freqs(b, a, logspace(-3, 3, 100))

    range_div = max(numpy.abs(h)) / min(numpy.abs(h))
    # print range_div
    var_1 = G / range_div;
    k = var_1 / min(numpy.abs(h))
    # rand = min(numpy.abs(h))
    # while (rand<1):
    #	rand = rand*10;
    #	power = power+1;

    w = w / 6
    # k = 1.1*10**(power+len(p_arr));
    # print k
    h = k * h
    # k = arange(0,127)
    # X = arange(0,0.5,0.001953125*2)
    # X = X*fs
    # X = k*fs/Nfft
    # Y = G*((numpy.fft.fft(b,Nfft)/numpy.fft.fft(a,Nfft)))
    # freq = ax[1].plot(X,(20*log10(numpy.abs((Y[0:128])))));

    freq = ax[1].plot(w, (numpy.abs(h)));
    ax[1].set_ylabel('Amplitude')
    # ax[1].set_ylabel('Magnitude (dB)')
    ax[1].set_xscale('log');
    ax[1].set_yscale('log');
    ax[1].set_xlim(Xmin, Xmax);

    axes(ax[2])
    plt.cla();
    # phase = ax[2].plot(X,180*((numpy.angle((Y[0:128]))))/3.1415);
    phase = ax[2].plot(w, 180 * (numpy.angle(h) / 3.1415));
    # phase = ax[2].plot(X,(numpy.angle((Y[0:128]))));
    ax[2].set_ylabel('Phase (degrees) ')
    ax[2].set_xlabel('Normalized Frequency (Hz)')
    ax[2].set_xscale('log');
    ax[2].set_ylim(-180, 180);
    ax[2].set_xlim(ax[1].get_xlim());


def zpgui(arg1=None, arg2=None, arg3=None):
    global fig, fig2, sslider

    def add_gain(event):
        global G
        gain = addgain.FormWidget()
        gain.show()
        app.exit(app.exec_())
        readfile = []
        for line in open('file.txt', 'r').readlines():
            if (line.strip() == ''):
                pass
            else:
                readfile.append(line.strip())
        gain = readfile[0]
        pos = 0
        if (gain == None):
            return
        else:
            G = float(gain)
        plotfilterchar()

    def set_range(event):
        global Xmin, Xmax
        if event.inaxes != ax[1]: return
        if event.button is 1:
            rfreq = rangefreq.FormWidget()
            rfreq.show()
            app.exit(app.exec_())
            readfile = []
            for line in open('file.txt', 'r').readlines():
                if (line.strip() == ''):
                    pass
                else:
                    readfile.append(line.strip())
            rfreq = readfile[0]
            pos = 0
            if (rfreq == None):
                return
            else:
                if (rfreq == ''):
                    return
                for i, val in enumerate(rfreq):
                    if (val == '-'):
                        pos = i
                Xmin = int(rfreq[0:pos])
                Xmax = int(rfreq[(pos + 1):len(rfreq)])
        # plotfilterchar()
        recompute()

    def onpick(event):
        global thisline
        if isinstance(event.artist, Line2D):
            thisline = event.artist

    def onmove(event):
        global thisline
        if event.inaxes != ax[0]: return
        if thisline is None: return
        axes(ax[0])
        objectlabel = thisline.get_label()
        objecttype = objectlabel[0]
        objectvalue = int(objectlabel[1]);
        if (objectvalue % 2):
            oppositevalue = objectvalue - 1;
            value = objectvalue / 2;
        else:
            oppositevalue = objectvalue + 1;
            value = (objectvalue + 1) / 2;

        if (objecttype == 'p'):
            plt.setp(ph[objectvalue], xdata=event.xdata, ydata=event.ydata)
            plt.setp(ph[oppositevalue], xdata=event.xdata, ydata=event.ydata * -1)
            # p[value] = round(event.xdata,4)+round(event.ydata,4)*1j
            p[value] = event.xdata + event.ydata * 1j

        else:
            plt.setp(zh[objectvalue], xdata=event.xdata, ydata=event.ydata)
            plt.setp(zh[oppositevalue], xdata=event.xdata, ydata=event.ydata * -1)
            # z[value] = round(event.xdata,4)+round(event.ydata,4)*1j
            z[value] = event.xdata + event.ydata * 1j

        # text = 'ZPGUI Version: ' + repr(version) + '      Selected Position: ' + repr(round(event.xdata,4)) + ' ' + repr(round(event.ydata,4)) + 'j';
        text = 'Selected Position: ' + repr(round(event.xdata, 4)) + ' ' + repr(round(event.ydata, 4)) + 'j';
        axtext.cla();
        axtext.text(1, -1.5, text, visible='True');

        recompute_only_fig1();

    def onrelease(event):
        global thisline
        thisline = None
        if event.inaxes != ax[0]: return
        recompute();

    def onfig1close(event):
        plt.close()

    def onfig2close(event):
        global fig2_closed, disable_3d_global
        fig2_closed = True;
        disable_3d_global = True;
        axfig2 = None

    def open3dwindow(event):
        global fig2, axfig2, disable_3d_global, z, p
        fig2 = plt.figure(figsize=plt.figaspect(0.75))
        fig2.canvas.mpl_connect('close_event', onfig2close)

        axfig2 = fig2.add_subplot(1, 1, 1, projection='3d')

        disable_3d_global = False;
        plot_z_surface(p, z, axfig2)
        show()

    def toggle_surface_display(event):
        global surface_toggle
        if (surface_toggle == 0):
            surface_toggle = 1;
        else:
            surface_toggle = 0;
        recompute();

    def addpole(event):
        global ph, ax, polecount, p

        readfile0 = []
        for line in open('polelist.txt', 'r').readlines():
            if (line.strip() == ''):
                pass
            else:
                readfile0.append(line.strip())
        a0 = polelist.FormWidget()
        a0.show()
        app.exit(app.exec_())
        temp0 = a0.get()
        readfile0 = temp0[len(readfile0):len(temp0)]
        temp0 = []
        for i, val in enumerate(readfile0):
            temp0.append(complex(val))

        for run in range(0, len(temp0), 1):
            plt.axes(ax[0])
            p.append(temp0[run])
            if (p[len(p) - 1].imag != 0):
                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, p[len(p) - 1].imag, 'x', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                ph.append(new_handler);

                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, p[len(p) - 1].imag * (-1), 'x', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                ph.append(new_handler);
                polecount = polecount + 2

            else:
                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, 0, 'x', ms=10)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                ph.append(new_handler);
                ph.append(new_handler);

                polecount = polecount + 2
        recompute();

    def addzero(event):

        global zh
        global ax
        global zerocount
        global z
        readfile1 = []
        for line in open('zerolist.txt', 'r').readlines():
            if (line.strip() == ''):
                pass
            else:
                readfile1.append(line.strip())
        a = zerolist.FormWidget()
        a.show()
        app.exit(app.exec_())
        temp = a.get()
        readfile1 = temp[len(readfile1):len(temp)]
        temp = []
        for i, val in enumerate(readfile1):
            temp.append(complex(val))
        for run in range(0, len(temp), 1):
            plt.axes(ax[0])
            z.append(temp[run])
            if (z[len(z) - 1].imag != 0):
                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, z[len(z) - 1].imag, 'wo', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                zh.append(new_handler);

                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, z[len(z) - 1].imag * (-1), 'wo', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                zh.append(new_handler);

            else:
                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, 0, 'wo', ms=10)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                zh.append(new_handler);
                zh.append(new_handler);

            zerocount = zerocount + 2
        # zplane(ax[0]);
        recompute();

    def removepole(event=None):
        global polecount, p, ph

        if (len(p) != len(ph) / 2):
            print
            'ERROR!'
        if (len(ph) != polecount):
            print
            'ERROR!'

        f = open('deletefile.txt', 'w')
        for i, val in enumerate(p):
            f.write(str(val) + '\n')
        f.close()
        temprp = delp.FormWidget()
        temprp.show()
        app.exit(app.exec_())
        temp1 = temprp.get()
        while (len(p) > 0):
            plt.setp(ph[polecount - 1], picker=None, visible=False)
            plt.setp(ph[polecount - 2], picker=None, visible=False)
            p.pop();
            polecount = polecount - 2;
            ph.pop();
            ph.pop();

        temp0 = []
        for i, val in enumerate(temp1):
            temp0.append(complex(val))
        for run in range(0, len(temp0), 1):
            plt.axes(ax[0])
            p.append(temp0[run])
            if (p[len(p) - 1].imag != 0):
                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, p[len(p) - 1].imag, 'x', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                ph.append(new_handler);

                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, p[len(p) - 1].imag * (-1), 'x', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                ph.append(new_handler);
                polecount = polecount + 2

            else:
                newlabel = 'p%d' % (polecount)
                new_handler = plt.plot(p[len(p) - 1].real, 0, 'x', ms=10)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                ph.append(new_handler);
                ph.append(new_handler);

                polecount = polecount + 2
        # zplane(ax[0]);
        recompute();

    def removezero(event):
        global zerocount, z, zh

        if (len(z) != len(zh) / 2):
            print
            'ERROR!'
        if (len(zh) != zerocount):
            print
            'ERROR!'

        f = open('deletefile.txt', 'w')
        for i, val in enumerate(z):
            f.write(str(val) + '\n')
        f.close()
        temprz = delp.FormWidget()
        temprz.show()
        app.exit(app.exec_())
        temp1 = temprz.get()
        while (len(z) > 0):
            plt.setp(zh[zerocount - 1], picker=None, visible=False)
            plt.setp(zh[zerocount - 2], picker=None, visible=False)
            z.pop();
            zerocount = zerocount - 2;
            zh.pop();
            zh.pop();

        temp = []
        for i, val in enumerate(temp1):
            temp.append(complex(val))
        for run in range(0, len(temp), 1):
            plt.axes(ax[0])
            z.append(temp[run])
            if (z[len(z) - 1].imag != 0):
                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, z[len(z) - 1].imag, 'wo', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                zh.append(new_handler);

                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, z[len(z) - 1].imag * (-1), 'wo', ms=10)
                plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5,
                         label=newlabel)
                zh.append(new_handler);

            else:
                newlabel = 'z%d' % (zerocount)
                new_handler = plt.plot(z[len(z) - 1].real, 0, 'wo', ms=10)

                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
                zh.append(new_handler);
                zh.append(new_handler);

            zerocount = zerocount + 2
        # zplane(ax[0]);
        recompute();

    f = open('ZPGUIDebug', 'w')

    global z, p, zh, ph, ax, press, polecount, zerocount, disable_3d_global

    if (arg1 is None) and (arg2 is None) and (arg3 is None):
        f.write('No arguments received, using default peramaters...\n')
        action = 'init';
        # z = [0.29-0.41j];
        # p = [-0.6+0.73j];
        z = [0 + 0j, 0 + 0j, -4.341e2 + 0j];
        p = [-3.691e-2 + 3.712e-2j, -3.712e2 + 0j, -3.739e2 + 4.755e2j, -5.884e2 + 1.508e3j, -3.691e-2 - 3.712e-2j,
             -3.739e2 - 4.755e2j, -5.884e2 - 1.508e3j];
    # z=[0j,0j,0j]
    # p=[-1,-3.03,-3.03,-313,-665]
    # z=[0j,0j]
    # p=[-3.852e-2+3.658e-2j,-3.852e-2-3.658e-2j,-1.78e2+0j,-1.35e2+1.6e2j,-1.35e2-1.6e+2j,-6.71e2+1.154e3j,-6.71e2-1.154e3j];
    elif (arg1 is not None) and (arg2 is not None):
        f.write('Two arguments received, using them for the pole and zero initial values...\n')
        action = 'init';
        p = arg1;
        z = arg2;
    else:
        action = arg1;

    surface_display_opts = 0;

    f.write('Plotting Figure...\n')
    # fig = plt.figure(figsize=plt.figaspect(0.75))
    fig = plt.figure('ZPGUI v' + repr(version))
    ax[0] = fig.add_subplot(3, 2, 1)

    axtext = axes([0.00, 1.05, 0.16, 0.075], visible='False')

    # text = 'ZPGUI Version: ' + repr(version);
    text = 'Selected Position: None'
    axtext.cla();
    axtext.text(1, -1.5, text, visible='True');

    f.write('Adding Buttons...\n')
    axaddpoles = axes([0.54, 0.83, 0.14, 0.05])
    baddpoles = Button(axaddpoles, 'Add Poles')
    baddpoles.on_clicked(addpole)

    axaddzeros = axes([0.71, 0.83, 0.14, 0.05])
    baddzeros = Button(axaddzeros, 'Add Zeros')
    baddzeros.on_clicked(addzero)

    axremovepoles = axes([0.54, 0.73, 0.14, 0.05])
    bremovepoles = Button(axremovepoles, 'Remove Poles')
    bremovepoles.on_clicked(removepole)

    axremovezeros = axes([0.71, 0.73, 0.14, 0.05])
    bremovezeros = Button(axremovezeros, 'Remove Zeros')
    bremovezeros.on_clicked(removezero)

    axtoggle = axes([0.71, 0.63, 0.14, 0.05])
    btoggle = Button(axtoggle, 'Toggle surface display')
    btoggle.on_clicked(toggle_surface_display)

    ax3d = axes([0.54, 0.63, 0.14, 0.05])
    b3d = Button(ax3d, 'Open 3D window')
    b3d.on_clicked(open3dwindow)

    axaddgain = axes([0.46, 0.73, 0.05, 0.05])
    baddgain = Button(axaddgain, 'New Gain')
    baddgain.on_clicked(add_gain)

    axes(ax[0])

    f.write('Plotting z-plane...\n')
    zplane(ax[0]);

    for i in arange(0, len(z), 1):
        if (z[i].imag != 0):
            newlabel = 'z%d' % (zerocount)
            # zh[i], = plt.plot(z[i].real, z[i].imag, 'wo', ms=10)
            new_handler = plt.plot(z[i].real, z[i].imag, 'wo', ms=10)
            plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5, label=newlabel)
            zh.append(new_handler)
            zerocount = zerocount + 1

            newlabel = 'z%d' % (zerocount)
            # zh[i+1], = plt.plot(z[i].real, z[i].imag*-1, 'wo', ms=10)
            new_handler = plt.plot(z[i].real, z[i].imag * -1, 'wo', ms=10)
            plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5, label=newlabel)
            zh.append(new_handler)
            zerocount = zerocount + 1
        else:
            newlabel = 'z%d' % (zerocount)
            new_handler = plt.plot(z[i].real, 0, 'wo', ms=10)
            # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
            # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
            zh.append(new_handler);
            zh.append(new_handler);
            zerocount = zerocount + 2

    for i in range(0, len(p), 1):
        if (p[i].imag != 0):
            newlabel = 'p%d' % (polecount)
            # ph[i], = plt.plot(p[i].real, p[i].imag, 'x', ms=10)
            new_handler = plt.plot(p[i].real, p[i].imag, 'x', ms=10)
            plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5, label=newlabel)
            ph.append(new_handler)
            polecount = polecount + 1

            newlabel = 'p%d' % (polecount)
            # ph[i+1], = plt.plot(p[i].real, p[i].imag*-1, 'x', ms=10)
            new_handler = plt.plot(p[i].real, p[i].imag * -1, 'x', ms=10)
            plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0, markeredgecolor='b', picker=5, label=newlabel)
            ph.append(new_handler)
            polecount = polecount + 1
        else:
            newlabel = 'p%d' % (polecount)
            new_handler = plt.plot(p[i].real, 0, 'x', ms=10)
            # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
            # plt.setp(new_handler, markersize=10.0, markeredgewidth=1.0,markeredgecolor='b',picker=5,label=newlabel)
            ph.append(new_handler);
            ph.append(new_handler);
            polecount = polecount + 2

    ax[1] = fig.add_subplot(3, 1, 2)
    ax[2] = fig.add_subplot(3, 1, 3)
    f.write('Plotting Characteristic...\n')
    plotfilterchar()

    fig.canvas.mpl_connect('pick_event', onpick)
    fig.canvas.mpl_connect('motion_notify_event', onmove)
    fig.canvas.mpl_connect('button_release_event', onrelease)
    fig.canvas.mpl_connect('close_event', onfig1close)
    fig.canvas.mpl_connect('button_press_event', set_range)
    # fig2.canvas.mpl_connect('close_event', onclose)

    f.write('Plot Complete.\n')
    show()


app = QApplication([])
zpgui()
# sys.exit(app.exec_())
