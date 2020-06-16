# Stuybuy
Tanzim Elahi, pd:5
features: light and tween.
instructions:
multiple lights can be used in an mdl script:
light (light_name) x y z r g b
the light command must be used at the very beginning of the mdl script.
one light must be given.
the tween command.
tween start_frame end_frame knoblist0 knoblist1
tween and vary can't be used in the same mdl script.
knoblist0 and knoblist1 must be given in the the format as shown below:
knobnameTValueSsecond_knobnameTvalue.....
For example if the knobnames are bigenetar and cake bigenetar:10 and cake:15, they have to be written as:
bigenetarT10ScakeT15
capital T and S are reserved letters and must not be used when naming knobs.
only one tween command can be used in a single mdl script.
