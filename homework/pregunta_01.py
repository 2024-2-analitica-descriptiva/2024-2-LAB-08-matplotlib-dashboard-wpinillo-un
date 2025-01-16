# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import pandas as pd
import matplotlib.pyplot as plt
import glob
import os


def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envios
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`

    * `Mode_of_Shipment`

    * `Customer_rating`

    * `Weight_in_gms`

    El dashboard generado debe ser similar a este:

    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png

    Para ello, siga las instrucciones dadas en el siguiente video:

    https://youtu.be/AgbWALiAGVo

    Tenga en cuenta los siguientes cambios respecto al video:

    * El archivo de datos se encuentra en la carpeta `data`.

    * Todos los archivos debe ser creados en la carpeta `docs`.

    * Su código debe crear la carpeta `docs` si no existe.

    """
    def load_data(file_path):
        return pd.read_csv(file_path)

    def plots(df, output_directory):
        def save_plots(output_directory, filename):
            folders = glob.glob(f"{output_directory}/*")
            if len(folders) >= 5:
                for file in folders:
                    os.remove(file)
                os.rmdir(output_directory)

            os.makedirs(output_directory, exist_ok=True)
            
            file_path = os.path.join(output_directory, filename)
            plt.savefig(file_path)

        def create_visual_for_shipping_per_warehouse(df, output_directory):
            """Visual for Shipping per Warehouse"""
            df = df.copy()
            counts = df.Warehouse_block.value_counts()
            plt.figure()
            counts.plot.bar(
                title="Shipping per Warehouse",
                xlabel="Warehouse block",
                ylabel="Record count",
                color="tab:blue",
                fontsize=8,
            )
            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)
            
            save_plots(output_directory, "shipping_per_warehouse.png")

        def create_visual_for_mode_of_shipment(df, output_directory):
            """Visual for Mode of Shipment"""
            df = df.copy()
            counts = df.Mode_of_Shipment.value_counts()
            plt.figure()
            counts.plot.pie(
                title="Mode of Shipment",
                wedgeprops=dict(width=0.35),
                ylabel="",
                colors=["tab:blue", "tab:orange", "tab:green"],
            )
            
            save_plots(output_directory, "mode_of_shipment.png")

        def create_visual_for_average_customer_rating(df, output_directory):
            """Visual for Average Customer Rating"""
            df = df.copy()
            df = (
                df[["Mode_of_Shipment", "Customer_rating"]]
                .groupby("Mode_of_Shipment")
                .describe()
            )
            df.columns = df.columns.droplevel()
            df = df[["mean", "min", "max"]]
            
            graph_settings = {
                "width": [df["max"].values - 1, df["mean"].values - 1],
                "height": [0.9, 0.5],
                "alpha": [0.8, 1.0],
                "color": [
                    "lightgray",
                    [
                        "tab:blue" if value >= 3.0 else "tab:orange"
                        for value in df["mean"].values
                    ],
                ],
            }
            
            plt.figure()
            for i in range(2):
                plt.barh(
                    y=df.index.values,
                    width=graph_settings["width"][i],
                    left=df["min"].values,
                    color=graph_settings["color"][i],
                    height=graph_settings["height"][i],
                    alpha=graph_settings["alpha"][i],
                )
                
            plt.title("Average Customer Rating")
            plt.gca().spines["left"].set_color("gray")
            plt.gca().spines["bottom"].set_color("gray")
            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

            save_plots(output_directory, "average_customer_rating.png")

        def create_visual_for_weight_distribution(df, output_directory):
            """Visual for Weight Distribution"""
            df = df.copy()
            plt.figure()
            df.Weight_in_gms.plot.hist(
                title="Shipped Weight Distribution",
                color="tab:orange",
                edgecolor="white",
            )
            plt.gca().spines["top"].set_visible(False)
            plt.gca().spines["right"].set_visible(False)

            save_plots(output_directory, "weight_distribution.png")

        plt.tight_layout()
        create_visual_for_shipping_per_warehouse(df, output_directory)
        create_visual_for_mode_of_shipment(df, output_directory)
        create_visual_for_average_customer_rating(df, output_directory)
        create_visual_for_weight_distribution(df, output_directory)

    def create_html(output_directory):
        """Create HTML"""
        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <style>
                    .card {
                        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                        transition: 0.3s;
                        border-radius: 5px;
                        margin: 10px;
                        padding: 10px;
                        background-color: #fff;
                    }
                    .card img {
                        border-radius: 5px;
                        width: 100%;
                    }
                </style>
            </head>
            <body>
                <h1>Shipping Dashboard</h1>
                <div style="width:45%;float:left">
                    <div class="card">
                        <img src="shipping_per_warehouse.png" alt="Fig 1">
                    </div>
                    <div class="card">
                        <img src="mode_of_shipment.png" alt="Fig 2">
                    </div>
                </div>
                <div style="width:45%;float:left">
                    <div class="card">
                        <img src="average_customer_rating.png" alt="Fig 3">
                    </div>
                    <div class="card">
                        <img src="weight_distribution.png" alt="Fig 4">
                    </div>
                </div>
            </body>
        </html>
        """

        file_path = os.path.join(output_directory, "index.html")
        with open(file_path, "w") as file:
            file.write(html)

    def generate_dashboard(output_directory):
        """Generate Dashboard"""
        df = load_data("files/input/shipping-data.csv")
        plots(df, output_directory)
        create_html(output_directory)

    generate_dashboard("./docs")
    print("Dashboard generado con éxito.")

if __name__ == "__main__":
    print(pregunta_01())

