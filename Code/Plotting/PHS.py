# =======  LIBRARIES  ======= #
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from HelperFunctions import stylize, set_figure_properties

# ============================================================================
# PHS (1D)
# ============================================================================


def PHS_1D_plot(events, data_sets):
    fig = plt.figure()
    title = 'PHS (1D)\nData set(s): ' + str(data_sets)
    xlabel = 'Counts'
    ylabel = 'Collected charge [ADC channels]'
    fig = stylize(fig, xlabel, ylabel, title, yscale='log', grid=True)
    plt.hist(events.ADC, bins=1000, range=[0, 4400], histtype='step',
             color='black', zorder=5)
    fig.show()


# =============================================================================
# PHS (2D)
# =============================================================================


def PHS_2D_plot(events, data_sets, module_order, number_of_detectors):
    def PHS_2D_plot_bus(fig, events, sub_title, vmin, vmax):
        xlabel = 'Channel'
        ylabel = 'Charge [ADC channels]'
        bins = [120, 120]
        fig = stylize(fig, xlabel, ylabel, title=sub_title, colorbar=True)
        plt.hist2d(events.Channel, events.ADC, bins=bins, norm=LogNorm(),
                   range=[[-0.5, 119.5], [0, 4400]], vmin=vmin, vmax=vmax,
                   cmap='jet')
        return fig

    fig = plt.figure()
    title = 'PHS (2D)\nData set(s): %s' % data_sets
    height = 12
    width = 14
    vmin = 1
    vmax = events.shape[0] // 1000
    for i, bus in enumerate(module_order):
        events_bus = events[events.Bus == bus]
        wire_events = events_bus[events_bus.Channel < 80].shape[0]
        grid_events = events_bus[events_bus.Channel >= 80].shape[0]
        plt.subplot(3, 3, i+1)
        sub_title = 'Bus: %d, events: ' % (bus, events_bus.shape[0])
        sub_title += ('\nWire events: %d, Grid events: %d'
                      % (wire_events, grid_events)
                      )
        fig = PHS_2D_plot_bus(fig, sub_title, events_bus, vmin, vmax)
    fig = set_figure_properties(fig, title, height, width)
    fig.show()

# =============================================================================
# PHS (Wires vs Grids)
# =============================================================================


def PHS_wires_vs_grids_plot(events, data_sets, module_order,
                            number_of_detectors):
    def charge_scatter(fig, events, sub_title, bus, vmin, vmax):
        xlabel = 'Collected charge wires [ADC channels]'
        ylabel = 'Collected charge grids [ADC channels]'
        bins = [200, 200]
        ADC_range = [[0, 5000], [0, 5000]]
        fig = stylize(fig, xlabel, ylabel, title=sub_title, colorbar=True)
        plt.hist2d(events.wADC, events.gADC, bins=bins,
                   norm=LogNorm(), range=ADC_range,
                   vmin=vmin, vmax=vmax, cmap='jet')
        return fig
    fig = plt.figure()
    title = 'PHS (Wires vs Grids)\nData set(s): %s' % data_sets
    height = 12
    width = 14
    vmin = 1
    vmax = events.shape[0] // 1000
    for i, bus in enumerate(module_order):
        events_bus = events[events.Bus == bus]
        sub_title = 'Bus %d\n(%d events)' % (bus, events_bus.shape[0])
        plt.subplot(3, 3, i+1)
        fig = charge_scatter(fig, events_bus, sub_title, bus, vmin, vmax)
    fig = set_figure_properties(fig, title, height, width)
    fig.show()