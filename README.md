# Modern Flask Dashboarding with Altair, Tailwind, Htmx, DuckDB, and more... 

## About
The purpose of this repo is to create a template of what a slim (< 250mb build for fast deployment on Vercel) flask application centered around dashboarding (interactive visuals powered by Altair (vega-light)), along with styling provided by Tailwind, could look like. 

In addition, some future modules will be added on in the future that explore DuckDB for doing very basic data processing, and HTMX as a replacement for requiring flask developers to have to perform any additional javascript. 

Trying to keep it basic. 

## Technology Stack
- **Webserver**: [Flask](https://flask.palletsprojects.com/)
- **Html**: [Htmx](https://htmx.org/) 
- **Styling**: [Tailwind](https://tailwindcss.com/) 
- **Visualizations**: [Altair](https://altair-viz.github.io/index.html) 
- **Local db**: [DuckDb](https://duckdb.org/) 

### Tailwind
- Took all of the elements out of box from [tailwind-ui](https://tailwindui.com/) and performed minimal modifications 

### Altair: Vega-Altair
- For some nice ideas, can play around with examples from: https://altair-viz.github.io/user_guide/compound_charts.html 


## To do
- Some github actions for:
    - Pytests
    - Linters 
    - Security 

