"""
The Dashboard module is responsible for the Performance Overview Dashboard,
accessible on the root endpoints of the web app.

This dashboard provides a visualization of CO2 over time, where each timeslot
is colored by the predicted IN_USE state of each timeslot.

The dashboard module is organized as follows:

- /dashboard/dashboard.html: The main HTML file that serves as the dashboard
  interface.
- /dashboard/plots: A subdirectory that holds room-specific data, organized by
  municipality, school, and room. Note that these .html documents are generated
  during model training.
- /dashboard/styles.css: The CSS file responsible for styling the dashboard.

## Dashboard Features

### Navigation
The dashboard provides navigation buttons to move between municipalities, schools,
and rooms, allowing users to explore different data points easily. Note that when
navigating between municipalities, the dashboard will display the first school in
the municipality, and when navigating between schools, the dashboard will display
the first room in the school.

### Displaying Plots
The dashboard dynamically loads and displays plots for selected rooms within the
iframe container. The plots are organized in the /plots directory. Note that the
dashboard relies on the endpoints in routes/dashboard.py to fetch plot data from
the server.

### Initialization
On startup, the dashboard fetches plot data from the server if any plots are
available in /dashboard/plots. It then displays the plots for the first room in
the first school in the first municipality.

### Customization
You can customize the dashboard's appearance and behavior by modifying the CSS in
styles.css and the HTML and JavaScript in dashboard.html. Additionally, you can
extend its functionality to suit your specific requirements.

### Why do we need this?
The Performance Overview Dashboard is a means of evaluation of our ML models. This
is useful, since the data available for this task is unlabelled, which means that
we cannot easily use quantitative metrics. As such, the web app will function
without this module, but it is a useful tool for evaluating the performance of
our models.
"""
