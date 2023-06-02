import matplotlib.colors as mc
import matplotlib.pyplot as plt
import numpy as np

# TODO: This is old code, must be fully redone

# Disable divide by zero warning (probably from single-occurrance avalanches)
np.seterr(divide = 'ignore') 

# https://stackoverflow.com/questions/16492830/colorplot-of-2d-array-matplotlib
# Graphics
def plot2dGrid(grid, key = None):
    
    #colors = [(0.6, 0.6, 0.6), (0.5, 0.5, 0.5), (0.4, 0.4, 0.4), (0.3, 0.3, 0.3), (0.2, 0.2, 0.2), (0.1, 0.1, 0.1), (0, 0, 0)]
    colors = [(0.6, 0.6, 0.6),  (0.4, 0.4, 0.4), (0.2, 0.2, 0.2), (0, 0, 0)]
    cmap  = mc.ListedColormap(colors)
    
    vmin, vmax = 0, 4
    
    # Main figure to display every component of the graph
    fig = plt.figure(figsize = (6, 5))

    # Main plot of the grid
    ax = fig.add_subplot(111)
    ax.set_title('colorMap')
    plt.imshow(grid, cmap = cmap, vmin = vmin, vmax = vmax)
    ax.set_aspect('equal')

    # Code for the color legend bar that is displayed next to the grid
    cax = fig.add_axes([0.22, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation = 'vertical', ticks = [0, 1, 2, 3], cmap = cmap)
    
    fig.savefig(f'grid{key}.png')
    plt.close()

# def plotAvalancheSizes(frequencies, sandStrategy, avalanches):
#     sizes, frequencyBySize, biggestSize = getAvalanceLogPlotData(frequencies)
    
#     fig = plt.figure(figsize = (7, 5))
#     ax = fig.add_subplot()
#     ax.set_title('A(n) vs n, ' + sandStrategy)
    
#     ax.plot(np.log10(sizes), np.log10(frequencyBySize))
#     ax.set_xlabel('log avalanche size')
#     ax.set_ylabel('log frequency')
    
    
#     plt.figtext(0.55, 0.8, 'Max size = ' + sizeToSmallText(biggestSize))
#     plt.figtext(0.55, 0.83, 'Tot avalanches = ' + sizeToSmallText(avalanches))
    
#     fig.savefig(f'log_log.png')
#     plt.close()

# def plotThreeSandStrategies(fRandom, fCenter, fEdge, avalanches):
#     rSize, rFreqBySize, rBiggestSize = getAvalanceLogPlotData(fRandom)
#     cSize, cFreqBySize, cBiggestSize = getAvalanceLogPlotData(fCenter)
#     eSize, eFreqBySize, eBiggestSize = getAvalanceLogPlotData(fEdge)
#     biggestSize = max(rBiggestSize,cBiggestSize,eBiggestSize)
    
#     fig = plt.figure(figsize = (7,5))
    
#     plt.plot(np.log10(rSize), np.log10(rFreqBySize), label='Random')
#     plt.plot(np.log10(cSize), np.log10(cFreqBySize), label='Center')
#     plt.plot(np.log10(eSize), np.log10(eFreqBySize), label='Edges')

#     plt.xlabel('log avalanche size')
#     plt.ylabel('log frequency')
#     plt.title('A(n) vs n, Random vs Center vs Edges')

#     plt.legend()
    
#     plt.figtext(0.4, 0.8, 'Max size = ' + sizeToSmallText(biggestSize))
#     plt.figtext(0.4, 0.83, 'Tot avalanches = ' + sizeToSmallText(avalanches))
    
#     fig.savefig(f'3log_log.png')
#     plt.close()

# # TODO: I don't like these datatype conversions, but they seem a necessary evil for using Python dictionaries
# def getAvalanceLogPlotData(frequencies):
#     sizes = np.sort(np.fromiter(frequencies.keys(), dtype = int))
#     frequencyBySize = np.fromiter(map(lambda size: frequencies[size], sizes), dtype = int)
#     biggestSize = sizes[sizes.size - 1]
#     return(sizes, frequencyBySize, biggestSize)

# def sizeToSmallText(number):
#     k = 1000
#     mil = 1000000
#     if number / k > 1 and number / k < k: return(str(round(number/k))+'k')
#     elif number / mil > 1 and number /mil < 10: return(str(round(number/mil, 1)) + 'million')
#     elif number / mil > 1 : return(str(round(number/ mil,0)) + 'million')
#     else: return(str(number))
