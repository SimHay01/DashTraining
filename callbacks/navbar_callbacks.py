# from dash import Input, Output
# from app import app

# # Callback used to highlight the name of the current page on your navbar.
# # If you are adding a new page to the application, please assign it the id "page-X" (with X the number following that of the previous pages) and add 1 to the upper bound of the range.
# # Add your condition and remember to add a "False" in the existing conditions   
# @app.callback([Output(f'page-{i}',"active") for i in range (1,4)],[Input("url","pathname")])
# def toggle_active_page(pathname):
#     if pathname in ["/"] or "/homepage" in pathname:
#         return True, False,False
#     elif "sourcing_table" in pathname:
#         return False, True,False
#     elif "archive" in pathname:
#         return False, False, True
#     else:
#         return False,False,False