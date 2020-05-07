# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:11:53 2020

@author: CJ ROCKBALL
"""

import numpy as np

from bokeh.layouts import gridplot, column, Spacer
from bokeh.models import CustomJS, Slider, TextInput, DataRange1d, LabelSet
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter
from bokeh.palettes import Spectral6

##  Create a table with (x, y) values of the graph... 
##              read x from slider

tabl = dict(gross=[1],
            income=[1],
            fixedc=[0],
            variablec=[0],
            dispinc=[0],
            savings=[0])

values = ColumnDataSource(tabl)

columns = [TableColumn(field="gross", title="Gross Income",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it')),
           TableColumn(field="income", title="Net Income",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it')),
           TableColumn(field="fixedc", title="Fixed Cost",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it')),
           TableColumn(field="variablec", title="Variable Cost",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it')),
           TableColumn(field="dispinc", title="Disposable Income",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it')),
           TableColumn(field="savings", title="Savings",formatter=NumberFormatter(format='0,0[.] ',text_align='left',language='it'))]

data_table = DataTable(source=values, columns=columns, editable=True)

## Create line graph
x = np.linspace(0, 10, 750)
y = np.ones((1,750))
source = ColumnDataSource(data=dict(x=x, y=y))

p1 = figure(plot_width=700, plot_height=350, y_range=DataRange1d(start = 0, end=None), x_range=DataRange1d(start = 0, end=None))
p1.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

p1.background_fill_color="#efefef"
p1.ygrid.band_fill_color = "olive"
p1.ygrid.band_fill_alpha = 0.1

### Create bar grpah
tabl2 = dict(name=['Gross Income', 'Net Income', 'Fixed Cost', 'Variable Cost', 'Disposable Income', 'Savings'], sum_size = [0,0,0,0,0,0],color=Spectral6)

values2 = ColumnDataSource(tabl2)

p2 = figure(plot_width=700, plot_height=350, x_range = values2.data["name"])

labels = LabelSet(x='name', y='sum_size', text='sum_size', level='glyph',
        x_offset=-13.5, y_offset=0, source=values2, render_mode='canvas')

p2.vbar(x='name',top='sum_size',color = 'color', width = 0.7, source=values2)

p2.background_fill_color="#efefef"
p2.ygrid.band_fill_color = "olive"
p2.ygrid.band_fill_alpha = 0.1
p2.add_layout(labels)


# Create sliders and in-data boxes
wd = 150
wd2 = 75

salary = TextInput(title="Gross Salary", value = str(1), width = wd)
tax_level = TextInput(title="Tax (%))", value = str(0), width = wd)
capital_gain = TextInput(title='Capital Gain', value = str(0), width = wd)
one_time_income = TextInput(title='One Time Income', value = str(0), width = wd)

rent_cost = TextInput(title="Rent", value= str(0), width = wd)
loan_cost = TextInput(title="Loan", value= str(0), width = wd)
utilities = TextInput(title="Utilities", value = str(0), width = wd)
insurance_cost = TextInput(title="Insurance", value = str(0), width = wd)
groceries = TextInput(title="Groceries", value = str(0), width = wd)
media_cost = TextInput(title="Media", value = str(0), width = wd)
clothing_cost = TextInput(title="Cloths", value = str(0), width = wd)
transport_cost = TextInput(title="Transportation", value = str(0), width = wd)
one_time_cost = TextInput(title="One Time Expense", value = str(0), width = wd)
exercise_hobby = TextInput(title="Exercise/Hobby", value = str(0), width = wd)

lunch_cost = TextInput(title="Lunch Cost", value = str(0), width = wd2)
rest_cost = TextInput(title="Restaurant Cost", value = str(0), width = wd2)
party_cost = TextInput(title="Party Cost", value = str(0), width = wd2)

lunch_slider = Slider(start=0, end=60, value=0, step=1, title="Lunch/Fast Food", width = wd)
rest_slider = Slider(start=0, end=10, value=0, step=1, title="Restaurant", width = wd)
party_slider = Slider(start=0, end=10, value=0, step=1, title="Party", width = wd)
offset_slider = Slider(start=0, end=10, value=0, step=1, title="Offset", width = wd)

# Update function 
callback = CustomJS(args=dict(source=source, values = values, values2=values2, \
                              tax=tax_level, sal=salary, capgain=capital_gain, otinc=one_time_income, \
                              rent=rent_cost, loan=loan_cost, util=utilities, insur=insurance_cost, \
                              lunch_cost=lunch_cost, rest_cost=rest_cost, party_cost=party_cost, \
                              groc=groceries, media=media_cost, cloth=clothing_cost, transp=transport_cost,exho=exercise_hobby,\
                              otexp=one_time_cost, lunc=lunch_slider, res=rest_slider, party=party_slider),
                    code="""
    const data = source.data;
    
    const S = sal.value;
    const t = tax.value;
    const Cg= - capgain.value;
    const Oti = - otinc.value;

    const Rn = rent.value;
    const Ln = loan.value;
    const Ut = util.value;
    const Ins = insur.value;
    const Gr = groc.value;
    const Med = media.value;
    const Cl = cloth.value;
    const Tr = transp.value;
    const Otc = otexp.value;
    const Ex = exho.value;
    
    const Lc = lunch_cost.value;
    const Rc = rest_cost.value;
    const Pc = party_cost.value;
    
    const A = lunc.value;
    const R = res.value;
    const P = party.value;
    
    const x = data['x']
    const y = data['y']
    
    values.data['gross'][0] = S - Cg - Oti;
    values.data['income'][0] = S*(1-t) - Cg - Oti;
    values.data['fixedc'][0] = -(0- Rn - Ln - Ut - Ins - Tr);
    values.data['variablec'][0] = -(0 - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc);
    values.data['dispinc'][0] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins;
    values.data['savings'][0] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc;

    values2.data['sum_size'][0] = S - Cg - Oti;    
    values2.data['sum_size'][1] = S*(1-t) - Cg - Oti; 
    values2.data['sum_size'][2] = -(0- Rn - Ln - Ut - Ins - Tr);
    values2.data['sum_size'][3] = -(0 - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc);
    values2.data['sum_size'][4] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins;
    values2.data['sum_size'][5] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc;
    
    for (var i = 0; i < 50; i++) {
        y[i] = S;
    }
    for (var i = 50; i < 100; i++) {
        y[i] = S - Cg;
    }
    for (var i = 100; i < 150; i++) {
        y[i] = S - Cg - Oti;
    }
    for (var i = 150; i < 200; i++) {
        y[i] = S*(1-t) - Cg - Oti;
    }
    for (var i = 200; i < 250; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins;
    }
    for (var i = 250; i < 300; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr;
    }
    for (var i = 300; i < 350; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr;
    }
    for (var i = 350; i < 400; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med;
    }
    for (var i = 400; i < 450; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl;
    }
    for (var i = 450; i < 500; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex;
    }
    for (var i = 500; i < 550; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc;
    }
    for (var i = 550; i < 600; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc;
    }
    for (var i = 600; i < 650; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc;
    }
    for (var i = 650; i < 700; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc;
    }
    for (var i = 700; i < x.length; i++) {
        y[i] = S*(1-t) - Cg - Oti - Rn - Ln - Ut - Ins - Tr - Gr - Med - Cl - Ex - Otc - A*Lc - R*Rc - P*Pc;
    }

    values.change.emit();
    values2.change.emit();
    source.change.emit();
""")

# call update function (callback) when the value in a box or slider is changed
for w in [salary, tax_level, capital_gain, one_time_income, \
          rent_cost, loan_cost, utilities, insurance_cost, groceries, media_cost, \
          clothing_cost, transport_cost, exercise_hobby,one_time_cost, \
          lunch_cost, rest_cost, party_cost,\
          lunch_slider, rest_slider,party_slider]:
    w.js_on_change('value', callback)

# Layout and disply functions
layout = column(gridplot([[salary, tax_level, capital_gain, one_time_income, rent_cost, loan_cost, utilities, insurance_cost, transport_cost], \
                          [groceries, media_cost, clothing_cost, exercise_hobby, one_time_cost], \
                          [lunch_cost, rest_cost, party_cost],[lunch_slider, rest_slider, party_slider]]),\
                            gridplot ([[p1, p2]]), gridplot ([[Spacer(width=735, height=0), data_table]]))

output_file("slider.html", title="slider.py example")

show(layout)









