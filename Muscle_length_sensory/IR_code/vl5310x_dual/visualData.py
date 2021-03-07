import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from readData import Data
from analysizeData import analyzeData


class plottingRoutine(Data):
    """
    This class does all kind of plotting depending on the method
    """

    # TODO: consider using bokeh for plotting

    def __init__(self, pathToFile, showPlots=False):
        """
        initialize input data. Expect a 3D array
        :param data:
        """
        if pathToFile is None:
            Exception('Need to give path to files')
        print('-> Create plotting routine object.')
        super().__init__(pathToFile=pathToFile)
        self.data = super().readData2Array()
        self.keys = super().returnKeys()
        self.showPlots = showPlots
        # define sampling period to make time array
        self.tPeriod = 0.093
        # get number of files
        self.z_len = len(self.data[0, 0, :])
        self.pathToFile = pathToFile

    def plotTimeSeries(self, showPlots=False, specificPlots=None):
        """
        Method to plot time series, input is time array.
        Define specific with a tuple of arrays that need to be plotted.
        :return:
        """
        print('>> Plot time series.')
        # create control array for for-loop
        controlArr = np.arange(self.z_len)
        assert isinstance(specificPlots, tuple), 'Plot selection must be a tuple'
        if specificPlots is None:
            for counter in controlArr:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
                axes.plot(time, self.data[:, 0, counter])
                axes.plot(time, self.data[:, 1, counter])
                axes.set_ylabel("Distance(mm)")
                axes.set_xlabel("Time (s)")
                axes.set_title(str(self.keys[counter]) + ' Plot')
        else:
            for counter in specificPlots:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
                axes.plot(time, self.data[:, 0, counter])
                axes.plot(time, self.data[:, 1, counter])
                axes.set_ylabel("Distance(mm)")
                axes.set_xlabel("Time (s)")
                axes.set_title(str(self.keys[counter]) + ' Plot')
        if showPlots:
            plt.show()

    def plotDiff(self, showPlots=False, specificPlots=None):
        """
        method to plot delta of the 2 sensors, input is time array
        :return:
        """
        print('>> Plot delta between sensors.')
        # create control array for for-loop
        controlArr = np.arange(self.z_len)
        if specificPlots is None:
            for counter in controlArr:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
                axes.plot(time, self.data[:, 0, counter] - self.data[:, 1, counter])
                axes.set_ylabel("Delta (mm)")
                axes.set_xlabel("Time (s)")
                axes.set_title(str(self.keys[counter]) + ' Plot')
        else:
            for counter in specificPlots:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
                axes.plot(time, self.data[:, 0, counter] - self.data[:, 1, counter])
                axes.set_ylabel("Delta (mm)")
                axes.set_xlabel("Time (s)")
                axes.set_title(str(self.keys[counter]) + ' Plot')
        if showPlots:
            plt.show()

    def plotSeriesLadder(self, showPlots=False, specificPlots=None):
        """
        Method to do ladder plot
        :return:
        """
        print(">> Generate ladder plot.")
        # create control array for for-loop
        controlArr = np.arange(self.z_len)
        assert isinstance(specificPlots, tuple), 'Plot selection must be a tuple'
        if specificPlots is None:
            fig, axes = plt.subplots(nrows=len(controlArr), ncols=1, figsize=(12, 5))  # generate template
            for counter in controlArr:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                axes[counter].plot(time, self.data[:, 0, counter])
                axes[counter].plot(time, self.data[:, 1, counter])
                axes[counter].set_ylabel("Distance(mm)")
                axes[counter].set_xlabel("Time (s)")
                axes[counter].set_title(str(self.keys[counter]) + ' Plot')
        else:
            fig, axes = plt.subplots(nrows=len(specificPlots), ncols=1, figsize=(12, 5))  # generate template
            axes[0].set_title('Plot ' + str(specificPlots))
            for counter in specificPlots:
                time = np.linspace(0, self.tPeriod * len(self.data[:, 0, 0]), len(self.data[:, 0, 0]))
                axes[specificPlots.index(counter)].plot(time, self.data[:, 0, counter])
                axes[specificPlots.index(counter)].plot(time, self.data[:, 1, counter])
                axes[specificPlots.index(counter)].set_ylabel("Distance(mm)")
                axes[specificPlots.index(counter)].set_xlabel("Time (s)")

        if showPlots:
            plt.show()

    def plotFit(self, fitOrder=3, fitSet=None, showPlots=False):
        """
        Method to plot the data and compare it with the fit.
        Call analyzeData class to calculate fit
        :param fitSet:
        :param fitOrder:
        :return:
        """
        analyzeDataInstance = analyzeData(self.pathToFile)
        fitCoeff, x2fit, y2fit = analyzeDataInstance.defineFit(fitOrder=fitOrder, fitSet=fitSet)
        # plot the fit
        poly1 = np.poly1d(fitCoeff)
        new_x = np.linspace(np.min(x2fit), np.max(y2fit))
        new_y = poly1(new_x)
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(x2fit, y2fit)  # scatter of fit data
        axes.plot(new_x, new_y, color="black", linewidth=2)  # line fit
        if showPlots is True:
            plt.show()
        return fitCoeff

    def showAllPlots(self):
        """
        Command to show all plots.
        :return:
        """
        plt.show()
