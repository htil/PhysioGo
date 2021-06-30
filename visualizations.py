
def linePlots(gui, count, color='#A54E4E', yMin=-20, yMax=20):
    layout = gui.addLayout()
    plots = []
    for i in range(count):
        p = layout.addPlot()
        p.setYRange(yMin, yMax)
        p = p.plot(pen='#A54E4E')
        plots.append(p)
        layout.nextRow()
    return plots
