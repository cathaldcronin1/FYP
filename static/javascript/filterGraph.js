$(document).ready(function()
{
    jQuery.extend(
        {
            filterData: function(language_filter)
            {
                var result = null;
                $.ajax(
                        {
                            url:  "/_filter_data",
                            type: "POST",
                            async : false,
                            data: JSON.stringify({"data": language_filter}),
                            contentType: "application/json; charset=utf-8",
                            success: function(response)
                            {
                                result = response;
                            }
                        });
                return result
            }
        });

    $('#filter').on('click', function()
    {
        var filters = [];
        var languageFilters = document.getElementsByTagName("input");

        for (var i = 0; i < languageFilters.length; i++)
        {
           // Take only those inputs which are checkbox
           if (languageFilters[i].checked)
           {
                filters.push(languageFilters[i].id);
           }
        }

        if (filters.length > 0)
        {
            // Clear the canvas and re initialise the graph.
            $("#canvas").empty();

            // Reinitialise the graph
            g = new Graph();

            // Filter data based on selected checkboxes //
            var filtered_result = $.filterData(filters)

            // Draw new graph with filtered data //
            for (var i = 0; i < filtered_result["value"].length; i++)
            {
                language_pair = filtered_result["value"][i]

                language1 = language_pair["connection"][0]
                language2 = language_pair["connection"][1]

                pair_connectivity = language_pair["count"]

                // Scaling factor is applied to standardise edge thicknesses.
                scale = (((pair_connectivity - min_language_count) / (max_language_count - min_language_count)) + 0.1) * 10

                g.addNode(language1, {render:render})
                g.addNode(language2, {render:render})
                g.addEdge(language1, language2 , { stroke : "#C0C0C0" , fill : "#56f", "stroke-width": scale});
            };


            /* layout the graph using the Spring layout implementation */
            layouter = new Graph.Layout.Spring(g);
            layouter.layout();

            /*draw the graph using the RaphaelJS draw implementation */
            renderer = new Graph.Renderer.Raphael(map_name, g, width, height);
            renderer.draw()
        };
    });
});
