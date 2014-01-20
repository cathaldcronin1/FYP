$(document).ready(function(){
var redraw;
var height = 500;
var width = 600;

window.onload = function()
{
     jQuery.extend(
     {
        getLanguages: function()
        {
            var result = null;
            $.ajax(
                    {
                        type: "GET",
                        url: $SCRIPT_ROOT + "/echo",
                        async : false,
                        contentType: "application/json; charset=utf-8",
                        success: function(data)
                        {
                              result = data;
                        }
                    });
            return result;
        }
    });

    /* Get all language information */
    var language = $.getLanguages();

    /* Create graph to draw nodes */
    var g = new Graph();

    /* Add a node */
    g.addNode(language.value.language)

    /* layout the graph using the Spring layout implementation */
    var layouter = new Graph.Layout.Spring(g);
    layouter.layout();

    /* draw the graph using the RaphaelJS draw implementation */
    var renderer = new Graph.Renderer.Raphael('canvas', g, width, height);
    renderer.draw();

    redraw = function()
    {
        layouter.layout();
        renderer.draw();
    };
};
});
