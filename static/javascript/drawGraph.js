var height = 1080;
var width = 1920;

map_name = "canvas";
var g = new Graph();
var render;
var snapshot;
var layouter;
var renderer;
var max_language_count;
var min_language_count;

jQuery.extend(
    {
        getNodeDetails: function(n, nodeId)
        {
            var result = null;
            $.ajax(
                    {
                        type: "POST",
                        url: $SCRIPT_ROOT + "/_get_node_details",
                        async : false,
                        data: JSON.stringify({"data": nodeId}),
                        contentType: "application/json; charset=utf-8",
                        success: function(data)
                        {
                              result = data;
                        }
                    });
            return result;
        }
    });

jQuery.extend(
{
    getLanguageInformation: function()
    {
        var result = null;
        $.ajax(
                {
                    type: "GET",
                    url: $SCRIPT_ROOT + "/_gather_graph_data",
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

jQuery.extend(
{
    refreshData: function()
    {
        var result = null;
        $.ajax(
                {
                    type: "GET",
                    url: $SCRIPT_ROOT + "/_refresh_data",
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


function popUp(n, nodeId)
{
    var nodeDetails = $.getNodeDetails(n, nodeId);
    var list_node_details = "";
    var node_info;
    var strongest_connection;

    for (var i = 1; i < nodeDetails["value"]["language_pairs"].length; i++)
    {
        node_info = nodeDetails["value"]["language_pairs"][i];
        if (node_info["connection"][0] === nodeId)
        {
            strongest_connection = node_info["connection"][1];
        }
        else
        {
            strongest_connection = node_info["connection"][0];
        }

        var count = node_info["count"];
        var item = "<li><b>{" + nodeId + ": " + strongest_connection + "}  - Occurrences: " + count + "</b></li>";

        list_node_details = list_node_details.concat(item);
    };

    // First element of nodeDetails is strongest_connection.
    var connection = nodeDetails["value"]["language_pairs"][0]["connection"];
    var count = nodeDetails["value"]["language_pairs"][0]["count"];

    if (connection[0] === nodeId)
    {
        strongest_connection = connection[1]
    }
    else
    {
         strongest_connection = connection[0]
    }

    $("#popupContainer").remove();

    // MODAL //

    // Container div
    var popupContainer = document.createElement('div');
    popupContainer.id = "popupContainer";
    popupContainer.className = "modal";

    // title
    var header = document.createElement('div');
    header.className = "modal-header";

    var exitButton = document.createElement('button');
    exitButton.type = "button";
    exitButton.className = "close";
    // exitButton.setAttribute("data-backdrop", "static");
    exitButton.setAttribute("data-dismiss", "modal");
    exitButton.innerHTML = "x";


    var title = document.createElement('h3');
    title.innerHTML = nodeId;

    header.appendChild(exitButton);
    header.appendChild(title);

    // body of pop up
    var popupContent = document.createElement('div');
    popupContent.className = 'modal-body';

    // content in body
    var content = document.createElement('p');
    console.log("nodelist" + list_node_details)
    // content.innerHTML ="Sed posuere consectetur est at lobortis. Aenean eu leo quam. Pellentesque ornare sem lacinia quam venenatis vestibulum.";
    content.innerHTML = "<li> <b>" + nodeId + " is Most Connected To: " + strongest_connection + "</b> </li>" +
                        "<li> <b>{" + nodeId + ": " + strongest_connection + "}  - Occurences: " + count + "</b> </li>" +
                        "<div class=\"panel panel-default\"> \
                             <div class=\"panel-heading\"> \
                                <h4 class=\"panel-title\"> \
                                    <a data-toggle=\"collapse\" data-parent=\"#accordion\" href=\"#collapseOne\" > \
                                        <b>Also Connected to</b> \
                                    </a> \
                                </h4> \
                            </div> \
                            <div id=\"collapseOne\" class=\"panel-collapse collapse\" style=\"height: auto;\"> \
                              <div id= \"panel\" class=\"panel-body\">"
                                + list_node_details +
                             "</div> \
                            </div> \
                        </div>";

    popupContent.appendChild(content);

    var footer = document.createElement('div');
    footer.className = 'modal-footer';

    var closeButton = document.createElement("button")
    closeButton.className = "btn";
    closeButton.innerHTML = "Close";
    closeButton.setAttribute("data-dismiss", "modal");


    footer.appendChild(closeButton);
    // END MODAL //

    popupContainer.appendChild(header);
    popupContainer.appendChild(popupContent);
    popupContainer.appendChild(footer);

    document.body.appendChild(popupContainer);


    $('#popupContainer').modal('show');
}

$(document).ready(function()
{
    render = function(r, n)
    {
        var nodeId = n.id;

        var color = Raphael.getColor();
        /* the Raphael set is obligatory, containing all you want to display */
        var set = r.set().push(
            r.ellipse(n.point[0], n.point[1]+10, 11, 11, nodeId)
            .attr({fill: color,
                   stroke: color,
                   "stroke-width": 3}))
            .push(r.text(n.point[0], n.point[1] + 30, nodeId)
                    .attr({"font-size":"16px",  "font-weight": "bolder"}));

        set.click( function()
        {
            popUp(n, nodeId);
        });
        return set;
    };
    var languageInfo;

    $('#refresh-data').click(function()
    {
        // Refresh data in backend
        languageInfo = $.refreshData();
        console.log("data refreshed")
    });


    /* Get all language information */
    languageInfo = $.getLanguageInformation();

    // Get language pairs and list of languages
    var language_pairs = languageInfo["value"]["language_pairs"]
    var languages = languageInfo["value"]["languages"]
    max_language_count = languageInfo["value"]["max_count"]
    min_language_count = languageInfo["value"]["min_count"]


    var col1 = document.getElementById("filter-col1");
    var col2 = document.getElementById("filter-col2");
    var col3 = document.getElementById("filter-col3");

    /* Create list of language checkboxes */
    for (var i = 0; i < languages.length; i++)
    {
        // picks a column for the language to go into
        var col_mod = i % 3;
        var label = document.createElement("label");
        label.setAttribute("class", "checkbox")

        var languageCheckbox = document.createElement("input");
        languageCheckbox.setAttribute("type","checkbox");
        languageCheckbox.setAttribute("id", languages[i]);
        languageCheckbox.checked=false

        var labeltext = document.createTextNode(languages[i]);

        label.appendChild(languageCheckbox)
        label.appendChild(labeltext)

        if (col_mod === 0) {
            col1.appendChild(label)
        };
        if (col_mod === 1) {
            col2.appendChild(label)
        };
        if (col_mod === 2) {
            col3.appendChild(label)
        };
    };

    /* Create graph to draw nodes */
    for (var pair in language_pairs)
    {
        var pairInformation = language_pairs[pair];
        language1 = pairInformation["connection"][0]
        language2 = pairInformation["connection"][1]

        pair_connectivity = pairInformation["count"]

        // Scaling factor is applied to standardise edge thicknesses.
        scale = (((pair_connectivity - min_language_count) / (max_language_count - min_language_count))) * 10

        g.addNode(language1, {label: language1, render:render})
        g.addNode(language2, {label: language2, render:render})
        g.addEdge(language1, language2 , { stroke : "#C0C0C0" , fill : "#56f", "stroke-width": scale});
    };

    /* layout the graph using the Spring layout implementation */
    layouter = new Graph.Layout.Spring(g);
    layouter.layout();

    /*draw the graph using the RaphaelJS draw implementation */
    renderer = new Graph.Renderer.Raphael(map_name, g, width, height);

    $('#filter-panel-button').click(function()
    {
        $("#filter-panel").toggleClass("hide");
    });
    $('#filter-panel-close-button').click(function()
    {
        $("#filter-panel").toggleClass("hide");
    });

    $("#filter-panel").draggable();
});
