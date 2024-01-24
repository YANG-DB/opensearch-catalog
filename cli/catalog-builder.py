import html
import json


def read_json(file_path):
    """Read and return JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)


def generate_html_for_section(data, section_title, item_key, modal=True, section_id="", modal_id_prefix=""):
    """Generate HTML content for a given section (Integrations or Visualizations)."""
    html_content = f"<h2 class='collapsible' onclick='toggleSection(\"{section_id}\")'>{section_title}</h2>"
    html_content += f"<div class='container content' id='{section_id}'><div class='row'>"

    for i, item in enumerate(data.get(item_key, [])):
        modal_id = f"{modal_id_prefix}{i}"  # Unique modal ID
        if i % 5 == 0 and i != 0:
            html_content += '</div><div class="row">'

        html_content += f"""
            <div class="col-md-2 grid-item text-center">
                <img src="{item.get('logo', '')}" style="width: 75px; height: 75px; cursor: pointer;" alt="{item.get('component', '')} Logo" data-toggle="modal" data-target="#modal{modal_id}">
                <p>{item.get('component', '')}</p>
            </div>
        """

        if modal:
            html_content += generate_modal_html(modal_id, item)

    html_content += "</div></div>"
    return html_content


def generate_modal_html(modal_id, item):
    """Generate HTML content for a modal."""
    try_me_url = item.get('try_me_url', '')  # URL for the "Try Me" feature
    try_me_url_encoded = html.escape(try_me_url)  # Encode special characters
    try_me_link_html = f"<div class='text-center'><a href='{try_me_url_encoded}' target='_blank' class='btn btn-primary'>Try Me</a></div>" if try_me_url_encoded else ""

    modal_html = f"""
        <div class="modal fade" id="modal{modal_id}" tabindex="-1" role="dialog" aria-labelledby="modalLabel{modal_id}" aria-hidden="true">
            <div class="modal-dialog modal-lg" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalLabel{modal_id}">{item.get('component', '')}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <img src="{item.get('logo', '')}" style="width: 100px; height: 100px;" alt="{item.get('component', '')} Logo">
                        <p><strong>Description:</strong> {item.get('description', '')}</p>
                        <p><strong>Version:</strong> {item.get('version', '')}</p>
                        <p><strong>URL:</strong> <a href="{item.get('url', '')}">{item.get('url', '')}</a></p>
                        {try_me_link_html}
                        <div>
                            {"".join([f'<img src="{asset.get("image", "")}" style="width: 100%; height: auto; margin-top: 10px;" alt="dashboard" />' for asset in item.get('gallery', [])])}
                        </div>
                        {generate_labels_html(item.get('tags', []))}
                    </div>
                </div>
            </div>
        </div>
    """
    return modal_html

def generate_css():
    """Generate and return CSS styles."""
    css_styles = """
    <style>
        .color-red { color: red; }
        .color-blue { color: blue; }
        .color-green { color: green; }
        .color-orange { color: orange; }
        .color-purple { color: purple; }
        .color-yellow { color: yellow; }
        .color-pink { color: pink; }
        .color-violet { color: violet; }
        .label-item {
            display: inline-block;
            margin-right: 10px;
        }
        body {
            font-family: Arial, sans-serif;
            background-color: #7e94ce;
            background-image: url('https://opensearch.org/assets/media/herobanners/release-hero-bg-mobile.png');
            background-size: cover;
            background-attachment: fixed;
            color: #ffffff;
        }
        .modal-content {
            background-color: #105179;
            background-image: url('https://opensearch.org/assets/media/herobanners/release-hero-bg-mobile.png');
            background-size: cover;
            background-attachment: fixed;
        }
        .container {
            max-width: 800px;
            padding: 8px; /* Add padding to the container */
        }
        .grid-item {
            border: 2px solid #8ea4de;
            padding: 5px;
            margin: 8px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            transform: perspective(500px) rotateY(0deg);
        }
        .grid-item:hover {
            background-color: #16415b;
            cursor: pointer;
            transform: scale(1.025);
            transform: perspective(500px) rotateY(20deg);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }
        h2 {
            text-align: center;
        }
        .collapsible {
            cursor: pointer;
        }
        .content {
            overflow: hidden;
            transition: max-height 0.2s ease-out;
            max-height: 1000px;
        }

    </style>
    """
    return css_styles


def generate_javascript():
    """Generate JavaScript for collapsible sections."""
    javascript = """
    <script>
        function showIframe(iframeId) {
            var iframe = document.getElementById(iframeId);
            iframe.style.display = iframe.style.display === 'none' ? 'block' : 'none';
        }
        function toggleSection(sectionId) {
            var content = document.getElementById(sectionId);
            if (content.style.maxHeight && content.style.maxHeight !== "1200px") {
                content.style.maxHeight = "1200px";
            } else {
                content.style.maxHeight = "0px";
            }
        }
    </script>
    """
    return javascript


def generate_labels_html(labels_data):
    """Generate HTML content for labels with specific colors and icons, displayed in a single row."""
    label_colors_icons = {
        "log": ("red", "▶"),
        "aws": ("blue", "⋔"),
        "communication": ("green", "❊"),
        "container": ("violet", "⤀"),
        "http": ("orange", "❖"),
        "cloud": ("purple", "✧"),
        "elb": ("yellow", "✑"),
        "url": ("pink", "❀")
    }

    labels_html = "<p><strong>Labels:</strong> "
    for label in labels_data:
        color, icon = label_colors_icons.get(label, ("black", "•"))  # Default color and icon
        labels_html += f"<span class='label-item color-{color}'><span class='label-icon'>{icon}</span> {label}</span> "

    labels_html += "</p>"
    return labels_html


def generate_catalog_details(integrations_data):
    """Generate HTML content for catalog details."""
    catalog_html = f"""
        <div class="container">
            <img src="{integrations_data.get('statics', {}).get('logo', {}).get('path', '')}" style="width: 750px; height: 250px;" alt="Logo" />
            <h1>{integrations_data.get('displayName', '')}</h1>
            <p><strong>Version:</strong> {integrations_data.get('version', '')}</p>
            <p><strong>URL:</strong> <a href="{integrations_data.get('url', '')}">{integrations_data.get('url', '')}</a></p>
            <p><strong>License:</strong> {integrations_data.get('license', '')}</p>
            <p><strong>Author:</strong> {integrations_data.get('author', '')}</p>
            {generate_labels_html(integrations_data.get('labels', []))}
        </div>
    """
    return catalog_html


def main():
    """Main function to generate the HTML content for the catalog."""
    integrations_data = read_json('../integrations/observability/catalog.json')
    visualizations_data = read_json('../visualizations/observability/widgets-catalog.json')

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OpenSearch Observability Catalog</title>
        <!-- Bootstrap CSS -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
        <!-- Bootstrap JS -->
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
       {generate_css()}
    </head>
    <body>
        {generate_catalog_details(integrations_data)}
        {generate_javascript()}
    """

    # Generate HTML for Integrations
    html_content += generate_html_for_section(integrations_data, 'Integrations', 'components', modal=True,
                                              section_id="integrations-section", modal_id_prefix="integ-")
    # Generate HTML for Visualizations
    html_content += generate_html_for_section(visualizations_data, 'Visualizations', 'components', modal=True,
                                              section_id="visualizations-section", modal_id_prefix="vis-")
    html_content += "</body></html>"

    # Write HTML content to file
    with open('catalog.html', 'w') as file:
        file.write(html_content)

    print("HTML file created successfully.")


if __name__ == "__main__":
    main()
