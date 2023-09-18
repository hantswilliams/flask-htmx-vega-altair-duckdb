# Modern Flask Dashboarding with Altair, Tailwind, Htmx, DuckDB, and more... 

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## About
The purpose of this repo is to create a template of what a slim (< 250mb build for fast deployment on Vercel) flask application centered around dashboarding (interactive visuals powered by Altair (vega-light)), along with styling provided by Tailwind, could look like. 

In addition, some future modules will be added on in the future that explore DuckDB for doing very basic data processing, and HTMX as a replacement for requiring flask developers to have to perform any additional javascript. 

Trying to keep it basic. 

But there ares still a few knwoledge requirements. First, an understanding of *Flask* and its *Flask Blueprints* feature; for ensuring a modular and well-organized application structure. Additionally, proficiency in some *HTML* (tags) and *CSS* (#), and then I decided on the Tailwind framework to simplify these styles. Finally, if deployment is on your horizon, it's beneficial to be familiar with Vercel, as it serves as our chosen platform for bringing the application live - and you can check out the deployment config file that lives in [vercel.json](vercel.json).

## Technology Stack
- **Webserver**: [Flask](https://flask.palletsprojects.com/)
- **Html**: [Htmx](https://htmx.org/) 
- **Styling**: [Tailwind](https://tailwindcss.com/) 
- **Visualizations**: [Altair](https://altair-viz.github.io/index.html) 
- **Local db**: [DuckDb](https://duckdb.org/) 

## Instructions for Creating Visuals 
### Understanding the Altair Chart Integration within the HTML File for Flask

Inside our [dashboard.html](src/templates/dashboard.html) file: 

```html
<div id="example-pointmap" class="overflow-hidden">
    <script>
        fetch('/data/altair/example/pointmap')
        .then(response => response.json())
        .then(data => {
            vegaEmbed('#example-pointmap', data);
        });
    </script>
</div>
```

In the provided HTML code snippet above, we're integrating an Altair graph into our webpage. Let's break down the process step by step:

1. **Data Source**: 
   - The data for the chart is not embedded directly within this HTML file. Instead, it's being fetched from an API endpoint: `/data/altair/example/pointmap`.
   - The code that serves this data resides in the Flask application, specifically under `src/modules/data`. Within this directory, we've set up various Altair graphs based on official examples.
   - We are generating the Altair output for each of the endpoints, and then jsonifying it 

2. **Fetching the Data with JavaScript**: 
   - The following JavaScript code makes an asynchronous request to the aforementioned API endpoint to retrieve the data for the graph:

     ```javascript
     fetch('/data/altair/example/pointmap')
     .then(response => response.json())
     .then(data => {
         vegaEmbed('#example-pointmap', data);
     });
     ```
   - Here's a breakdown of the JavaScript:
     - `fetch('/data/altair/example/pointmap')`: This sends an HTTP request to the given endpoint.
     - `.then(response => response.json())`: Once the data is received, this line ensures it's parsed as JSON.
     - `.then(data => {...})`: After parsing, the data is passed to the `vegaEmbed` function, which takes care of rendering the graph.

3. **Rendering the Chart**: 
   - To display the graph, we use a `<div>` element with the id `example-pointmap`.
   - The `vegaEmbed` function (from the Vega-Lite library that Altair builds upon) is called with the id (`#example-pointmap`) of the `<div>` where the graph should be rendered, as well as the data for the graph.
   - Thanks to this function, the graph will be displayed inside the `<div>` with the specified id.

In summary, this setup allows for a clean separation of concerns. The Flask application manages the data and graph generation, while the HTML and JavaScript handle the presentation and rendering of the graph on the webpage.

---

## To do
- [ ] Add in basic user login, simple RBAC 
- Some github actions for:
    - [ ] Pytests
    - [x] Lint with [Black](https://black.readthedocs.io/) 
    - [ ] Security 

