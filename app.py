import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
import palmerpenguins
import seaborn as sns
from shiny import render
import shinyswatch
from shiny import reactive

penguins_df = palmerpenguins.load_penguins()

ui.page_opts(title="Cera's Palmer Penguins Data", fillable=True)
with ui.sidebar(open = "open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
    )
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 50)
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 0, 100, 50)
    ui.input_checkbox_group("selected_species_list", "List of Selected Species", ["Adelie", "Gentoo", "Chinstrap"],selected= ["Gentoo"], inline= False)
    ui.hr()
    ui.input_checkbox_group("selected_island_list", "List of Selected Islands", ["Torgerson", "Biscoe", "Dream"], selected= ["Dream"], inline= False)
    ui.a("Cera's GitHub", href= "https://github.com/ceradrake/cintel_02-data/tree/main", target= "_blank")

#Data Table and Data Grid
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Penguin Data Table")
    @render.data_frame
    def penguins_datatable():
        return render.DataTable(filtered_data())
    ui.h2("Penguin Data Grid")
    @render.data_frame
    def penguins_datagrid():
        return render.DataGrid(filtered_data())

#Plotly Histogram
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Species Histogram")
    @render_plotly
    def plotly_histogram():
        return px.histogram(filtered_data(), x="bill_length_mm",
                color="species")
#Seaborn Histogram
ui.h2("Seaborn Histogram")
@render.plot
def plot_sns():
 return sns.histplot(filtered_data(), x="body_mass_g", hue = 'species')

#Plotly Scatterplot
with ui.card(full_screen = True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(
            filtered_data(), x="body_mass_g", y="flipper_length_mm", color = "species", symbol = "sex", title = "Body Mass based on Sex and Species"
        )
    
shinyswatch.theme.journal()
@reactive.calc
def filtered_data():
    return penguins_df[penguins_df["species"].isin(input.selected_species_list())]
