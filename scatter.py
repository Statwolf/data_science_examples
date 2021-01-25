from data_science.plot.plot_base import Plot
from data_science.plot.column import Column 

import plotly.graph_objs as go


class Scatter(Plot):
    '''
    Builds a scatter plot

    Can be both 2D or 3D 
    '''
    def __init__(self, dataframe, dim=2):
        '''
        Parameters:
        -----------
        dataframe: pandas.DataFrame
            the dataframe to plot.
        dim: int (2 or 3)
            2 for 2D plot, 3 for 3D plot.
        '''
        self._dim = dim
        self._hue = None
        self._text = None
        # lines in the plot
        self._lines = []
        super(Scatter, self).__init__(dataframe)
        self._x = None
        self._y = None
        self._z = None
        

    def _default_settings(self):
        '''
        Sets the default settings
        '''
        common_settings = {
            'name': None,
            # the type of scatter
            'mode': 'markers',
            # sets the marker opacity
            'opacity': 0.8,
            'marker': {
                # the size of the marker
                'size': 6 if self._dim == 2 else 4,
                # the color (or colors) of the marker
                'color': '#23459b',
                # the symbol for the marker
                'symbol': 'circle'
            },
            'line': {
                'shape': 'linear',
                'dash': 'solid',
                'width': 2
            } if self._dim == 2  else {}, # only for 2D
            'classes': [],
            # group for legend
            'legendgroup': None,
            # if to show the legend
            'showlegend': True,
        }

        if self._dim == 2:
            # if to fill with the previous scatter
            common_settings['fill'] = None

        return common_settings

    def line(self, X, Y, Z=None, settings={}):
        '''
        Draw a line

        Parameters:
        -----------
        X: list or ndarray
            \tA list of len 2 (or 3 for 3D scatter) that contains 2 point in the x-axis.
        Y: list or ndarray
            \tA list of len 2 (or 3 for 3D scatter) that contains 2 point in the y-axis.
        settings: dict
            The settings for the actual threshold. Same settings of the global scatter traces.
            \t\n The default settings are the same of the global scatter traces except for:
            \t\n - mode: 'lines'
            \t\n - line: 'dash'
            \t\n - legendgroup: 'threshold'
            \t\n - showlegend: True only for first threshold
        '''
        actual_settings = self._default_settings()
        actual_settings['mode'] = 'lines'
        actual_settings['line']['dash'] = 'dash'
        actual_settings['legendgroup'] = 'thresholds'
        actual_settings['showlegend'] = False if self._lines else True
        actual_settings.update((k, settings[k]) for k in actual_settings.keys() & settings.keys())

        self._lines.append({
            'X': X,
            'Y': Y,
            'settings': actual_settings
        })        
        return self

    def hue(self, column):
        '''
        Set which column of the dataset use to color.
        '''
        self._hue = column
        return self

    def text(self, column='', is_index=False):
        '''
        Set which column (or index) of the dataset use as label.
        '''
        self._text = Column(column=column, is_index=is_index)
        return self

    def x(self, column='', is_index=False):
        '''
        Set which column (or index) of the dataset plot on X-axis.
        '''
        self._x = Column(column=column, is_index=is_index)
        return self
        
    def y(self, column='', is_index=False):
        '''
        Set which column (or index) of the dataset plot on Y-axis.
        '''
        self._y = Column(column=column, is_index=is_index)
        return self
    
    def z(self, column='', is_index=False):
        '''
        Set which column (or index) of the dataset plot on Z-axis.
        '''
        self._z = Column(column=column, is_index=is_index)
        return self

    def settings(self, settings={}):
        '''
        Set the settings for the specific plot.

        Parameters:
        -----------
        settings: {} global settings
            'name': str 
                the name of the trace, if classes is not None, it will be overwritten
            'mode': str (default "markers", Any combination of "lines", "markers", "text" joined with a "+" OR "none")
                Determines the drawing mode for this scatter trace. If the provided `mode` includes "text" then the `text` elements appear at the coordinates. Otherwise, the `text` elements appear on hover. If there are less than 20 points and the trace is not stacked then the default is "lines+markers". Otherwise, "lines".
            'opacity': int or [int] (between or equal to 0 and 1)
                    sets the marker opacity
            'marker': {} the marker
                'size': int (default: 6 for 2D, 2 for 3D)
                    the size of the marker
                'color': str or [str]
                    the color (or colors) of the marker
                'symbol': str (default "circle")
                    the symbol for the color
            'line': {} the line
                'shape': -FOR 2D SCATTER ONLY-, str (default "linear", ["linear" | "spline" | "hv" | "vh" | "hvh" | "vhv"])
                    Determines the line shape. With "spline" the lines are drawn using spline interpolation. The other available values correspond to step-wise line shapes.
                'dash': str (default: "solid")
                    Sets the dash style of lines. Set to a dash type string ("solid", "dot", "dash", "longdash", "dashdot", or "longdashdot") or a dash length list in px (eg "5px,10px,2px,2px").
                'width': int (default 2)
                    Sets the line width
            'classes': [{}] an array of dict, for each class
                'name': str
                    the name of the class, needs to be a value in the column: self._dataset[self._hue]
                'color': str
                    the color of the actual class
                'symbol': str
                    the symbol for the marker
                'size': int
                    size of the marker
            'legendgroup': str, (default None)
                The group for the legends (filters will be applicate all togheter).
            'showlegend': bool, (default True)
                Indicates if to show this trace in legend.
            'fill': str, (default None)
                One of ( "none" | "tozeroy" | "tozerox" | "tonexty" | "tonextx" | "toself" | "tonext" ).
                Sets the area to fill with a solid color. Defaults to "none" unless this trace is stacked, then it gets "tonexty" ("tonextx") if `orientation` is "v" ("h") Use with `fillcolor` if not "none". "tozerox" and "tozeroy" fill to x=0 and y=0 respectively. "tonextx" and "tonexty" fill between the endpoints of this trace and the endpoints of the trace before it, connecting those endpoints with straight lines (to make a stacked area graph); if there is no trace before it, they behave like "tozerox" and "tozeroy". "toself" connects the endpoints of the trace (or each segment of the trace if it has gaps) into a closed shape. "tonext" fills the space between two traces if one completely encloses the other (eg consecutive contour lines), and behaves like "toself" if there is no trace before it. "tonext" should not be used if one trace does not enclose the other. Traces in a `stackgroup` will only fill to (or be filled to) other traces in the same group. With multiple `stackgroup`s or some traces stacked and some not, if fill-linked traces are not already consecutive, the later ones will be pushed down in the drawing order.
        '''
        self._settings.update((k, settings[k]) for k in self._settings.keys() & settings.keys())
        return self

    def _get_class_names(self):
        '''
        Retrieve (if exists) all the class name in the settings.
        '''
        class_names = []
        for c in self._settings['classes']:
            class_names.append(c['name'])

        return class_names

    def _get_class_settings(self, class_name):
        '''
        Retrieve the settings for a specific class.

        Parameters:
        -----------
        class_name: str
            the class to search.
        '''
        if class_name in self._get_class_names():
            for s in self._settings['classes']:
                if s['name'] == class_name:
                    return s
        
        return {}

    def _get_legendgroup_settings(self, class_name):
        '''
        Retrieve the legendgroup for a specific class.

        Parameters:
        -----------
        class_name: str
            the class to search.
        '''
        if type(self._settings['legendgroup']) is dict:
            legend_group = self._settings['legendgroup'][class_name]
        else:
            legend_group = self._settings['legendgroup']
        
        return legend_group            

    def _build(self):
        '''
        Contains the logic to create the plot.
        '''
        traces = []

        if self._x and self._y:

            if self._hue is None:
                traces = [
                            go.Scatter(
                                        x=self._x.get_column_value(self._dataframe),
                                        y=self._y.get_column_value(self._dataframe),
                                        mode=self._settings['mode'],
                                        opacity=self._settings['opacity'],
                                        marker=self._settings['marker'],
                                        line=self._settings['line'],
                                        name=self._settings['name'], 
                                        text=None if self._text is None else self._text.get_column_value(self._dataframe),
                                        legendgroup=self._settings['legendgroup'],
                                        showlegend=self._settings['showlegend'],
                                        fill=self._settings['fill']
                            ) \
                            if self._dim == 2 else \
                            go.Scatter3d(
                                        x=self._x.get_column_value(self._dataframe),
                                        y=self._y.get_column_value(self._dataframe),
                                        z=self._z.get_column_value(self._dataframe),
                                        mode=self._settings['mode'],
                                        opacity=self._settings['opacity'],
                                        marker=self._settings['marker'],
                                        line=self._settings['line'],
                                        name=self._settings['name'],
                                        text=None if self._text is None else self._text.get_column_value(self._dataframe),
                                        legendgroup=self._settings['legendgroup'],
                                        showlegend=self._settings['showlegend'],
                            )
                        ]
            else:
                # get all class name in settings
                class_names = self._get_class_names()

                # need to color different classes
                for actual_class in self._dataframe[self._hue].unique():
                    tmp_df = self._dataframe.loc[self._dataframe[self._hue] == actual_class]

                    # remove color, in this way for each class 
                    # plotly set a default color
                    if 'color' in self._settings['marker']:
                        del self._settings['marker']['color']

                    marker = self._settings['marker'].copy()

                    legendgroup = self._get_legendgroup_settings(actual_class)

                    # check if we have specific setting for actual class
                    if actual_class in class_names:
                        actual_settings = self._get_class_settings(actual_class)
                        marker['color'] = actual_settings['color']
                        marker['symbol'] = actual_settings['symbol']
                        marker['size'] = actual_settings['size']
                    
                    traces.append(
                                    go.Scatter(
                                                x=self._x.get_column_value(tmp_df),
                                                y=self._y.get_column_value(tmp_df),
                                                mode=self._settings['mode'],
                                                opacity=self._settings['opacity'],
                                                name=str(actual_class),
                                                marker=marker,
                                                line=self._settings['line'],
                                                text=None if self._text is None else self._text.get_column_value(tmp_df),
                                                legendgroup=legendgroup,
                                                showlegend=self._settings['showlegend'],
                                                fill=self._settings['fill']
                                    ) \
                                    if self._dim == 2 else \
                                    go.Scatter3d(
                                                x=self._x.get_column_value(tmp_df),
                                                y=self._y.get_column_value(tmp_df),
                                                z=self._z.get_column_value(tmp_df),
                                                mode=self._settings['mode'],
                                                opacity=self._settings['opacity'],
                                                name=str(actual_class),
                                                marker=marker,
                                                line=self._settings['line'],
                                                text=None if self._text is None else self._text.get_column_value(tmp_df),
                                                legendgroup=self._settings['legendgroup'],
                                                showlegend=self._settings['showlegend'],
                                    ) 
                                )

        for thr in self._lines:
            traces.append(
                go.Scatter(
                            x=thr['X'],
                            y=thr['Y'],
                            mode=thr['settings']['mode'],
                            opacity=thr['settings']['opacity'],
                            name=thr['settings']['name'],
                            marker=thr['settings']['marker'],
                            line=thr['settings']['line'],
                            legendgroup=thr['settings']['legendgroup'],
                            showlegend=thr['settings']['showlegend'],
                            fill=thr['settings']['fill']
                ) \
                if self._dim == 2 else \
                go.Scatter3d(
                            x=thr['X'],
                            y=thr['Y'],
                            z=thr['Z'],
                            mode=thr['settings']['mode'],
                            opacity=thr['settings']['opacity'],
                            name=thr['settings']['name'],
                            marker=thr['settings']['marker'],
                            line=thr['settings']['line'],
                            legendgroup=thr['settings']['legendgroup'],
                            showlegend=thr['settings']['showlegend'],
                            fill=thr['settings']['fill']
                )
            )
                
        return traces

