import plotly.graph_objects as go
import pandas as pd

def create_metric_animation(df):
    df.loc[df['frameId']>df.loc[df['Pt']>=1,'frameId'].min(),'Pt'] = 1

    trace1 = go.Scatter(x=df.frameId[:2],
                        y=df.dist[:2],
                        mode='lines',
                        line=dict(width=3),
                        yaxis='y1',
                        line_color='blue',
                       )

    trace2 = go.Scatter(x = df.frameId[:2],
                        y = df.Pt[:2],
                        mode='lines',
                        line=dict(width=3),
                        yaxis='y2',
                        line_color='red',
                       )

    frames = [dict(data= [dict(type='scatter',
                               x=df.frameId[:k+1],
                               y=df.dist[:k+1],
                               yaxis='y1',
                               mode='lines',
                               line_color='blue',
                              ),
                          dict(type='scatter',
                               x=[df.frameId[k]],
                               y=[df.dist[k]],
                               yaxis='y1',
                               mode='markers+text',
                               marker=dict(color='blue',size=10),
                               text=f"{df.dist.iloc[k]:0.1f}",
                               textposition='bottom right',
                               textfont_color='blue',
                              ),
                          dict(type='scatter',
                               x=df.frameId[:k+1],
                               y=df.Pt[:k+1],
                               yaxis='y2',
                               mode='lines',
                               line_color='red',
                              ),
                          dict(type='scatter',
                               x=[df.frameId[k]],
                               y=[df.Pt[k]],
                               yaxis='y2',
                               mode='markers+text',
                               marker=dict(color='red',size=10),
                               text=f"{df.Pt.iloc[k]:0.2f}",
                               textposition='bottom right',
                               textfont_color='red',
                              ),
                         ],
                   traces= [0, 1, 2, 3],  #this means that  frames[k]['data'][0]  updates trace1, and   frames[k]['data'][1], trace2 
                  )for k in range(1, len(df)-1)] 

    layout = go.Layout(width=1000,
                       height=600,
                       yaxis=dict(title='DISTANCE TO BALLCARRIER'),
                       yaxis2=dict(title='EXPECTED APPROACH PROBABILITY',overlaying='y',side='left',position=0.1),
                       showlegend=False,
                       hovermode='closest',
                       updatemenus=[dict(type='buttons', showactive=False,
                                    y=1.05,
                                    x=1.3,
                                    xanchor='right',
                                    yanchor='top',
                                    pad=dict(t=0, r=10),
                                    buttons=[dict(label='Play',
                                                  method='animate',
                                                  args=[None, 
                                                        dict(frame=dict(duration=500, 
                                                                        redraw=False),
                                                             transition=dict(duration=0),
                                                             fromcurrent=True,
                                                             mode='immediate')]),
                                             {"args": [[None], {"frame": {"duration": 0, "redraw": False},"mode": "immediate","transition": {"duration": 0}}],
                                              "label": "Pause",
                                              "method": "animate"}
                                            ])])
    layout.update(
        xaxis=dict(range=[df.frameId[0], df.frameId[len(df)-1]], autorange=False, title='FRAME'),
        yaxis=dict(range=[-1,11], autorange=False),
        yaxis2=dict(range=[-0.1,1.1], autorange=False,),
    )
    fig = go.Figure(data=[trace1, trace1, trace2, trace2], frames=frames, layout=layout)
    for i in range(len(df)):
        event_for_frame = df['event'].iloc[i]
        if pd.notna(event_for_frame):
            plot_text = event_for_frame.replace('_',' ').upper()
            fig.add_vline(x=df['frameId'].iloc[i], line_width=1, line_dash="dash", line_color="black", annotation_text=plot_text)
    fig.add_hline(y=1, line_width=3, line_dash='dash',line_color='blue')
    fig.show()