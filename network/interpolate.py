import os













def interpolate_data():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    input_dir = os.path.join(os.path.pardir, "data", "flight_csvs")
    output_csvs_dir = os.path.join(os.path.pardir, "data", "flight_csvs_interpolated")

    
