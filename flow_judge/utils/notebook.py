from IPython.display import HTML, display


def is_notebook() -> bool:
    """Check if the current environment is a Jupyter notebook.

    Returns:
        bool: True if in a notebook, False otherwise.
    """
    try:
        return get_ipython().__class__.__name__ == "ZMQInteractiveShell"
    except NameError:
        return False


def request_rubric(
    title: str,
    description: str,
    similar_to: str | None = None,
    custom_fields: dict[str, str] | None = None,
):
    """Create a new rubric request and open it in the browser or display it in a notebook.

    Args:
        title (str): Title of the rubric request.
        description (str): Description of the rubric request.
        similar_to (str | None): Name of a similar existing rubric.
        custom_fields (dict[str, str] | None): Additional custom fields for the request.
    """
    pass


#     issue_title = f"Rubric Request: {title}"
#     templates = load_rubric_templates("example_rubrics")
#     similar_template = templates.get(similar_to, None) if similar_to else None

#     issue_body = f"""
# ## Rubric Request

# **Title:** {title}

# **Description:**
# {description}

# ## Similar Rubric
# {f"This request is similar to the existing rubric: `{similar_to}`" if similar_to else "N/A"}

# ## Proposed Structure
# ```yaml
# name: {title.lower().replace(' ', '_')}
# description: {description}
# criteria: [TO BE FILLED]
# rubric:
#   - score: 0
#     description: [TO BE FILLED]
#   - score: 1
#     description: [TO BE FILLED]
# required_inputs: {similar_template.required_inputs if similar_template else '[TO BE FILLED]'}
# required_output: {similar_template.required_output if similar_template else '[TO BE FILLED]'}
# ```

# ## Additional Information
# {yaml.dump(custom_fields) if custom_fields else "Please provide any additional context"
#  " or requirements for this rubric."}

# ## Existing Rubrics for Reference
# {yaml.dump({name: template.description for name, template in templates.items()})}
# """

#     encoded_body = quote(issue_body)
#     url = f"https://github.com/flowaicom/flow-judge/issues/new?title={quote(issue_title)}&body={encoded_body}&labels=enhancement,rubric-request"

#     if is_notebook():
#         display(
#             HTML(
#                 f"""
#         <a href="{url}" target="_blank">
#             <button style="background-color: #4CAF50; border: none; color: white; padding: "
#             "15px 32px; text-align: center; text-decoration: none; display: inline-block; "
#             "font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px; "
#             "box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);">
#                 Create New Rubric Request
#             </button>
#         </a>
#         """
#             )
#         )
#     else:
#         webbrowser.open(url)
#         print("Browser opened with the rubric request creation page.")


def display_rubric_request_form():
    """Display an interactive form for creating rubric requests in a Jupyter notebook."""
    # templates = load_rubric_templates("example_rubrics")
    # options = "".join([f'<option value="{name}">{name}</option>' for name in templates.keys()])
    options = "placeholder"

    form_html = f"""
    <form id="rubricForm" style="max-width: 500px; margin: 20px auto; padding: 20px; border: "
    "1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div style="margin-bottom: 15px;">
            <label for="title" style="display: block; margin-bottom: 5px;">Rubric Title:</label>
            <input type="text" id="title" name="title" required style="width: 100%; padding: 8px;"
            " border: 1px solid #ccc; border-radius: 4px;">
        </div>
        <div style="margin-bottom: 15px;">
            <label for="description" style="display: block; margin-bottom: 5px;">Description:"
            "</label>
            <textarea id="description" name="description" required style="width: 100%; "
            "height: 100px; padding: 8px; border: 1px solid #ccc; border-radius: 4px;"></textarea>
        </div>
        <div style="margin-bottom: 15px;">
            <label for="similarTo" style="display: block; margin-bottom: 5px;">Similar to existing"
            " rubric:</label>
            <select id="similarTo" name="similarTo" style="width: 100%; padding: 8px; border:"
            " 1px solid #ccc; border-radius: 4px;">
                <option value="">Select a rubric</option>
                {options}
            </select>
        </div>
        <button type="submit" style="background-color: #4CAF50; border: none; color: white;"
        " padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block;"
        " font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
            Create Rubric Request
        </button>
    </form>
    <div id="result"></div>
    <script>
    document.getElementById('rubricForm').addEventListener('submit', function(e) {{
        e.preventDefault();
        var title = document.getElementById('title').value;
        var description = document.getElementById('description').value;
        var similarTo = document.getElementById('similarTo').value;

        IPython.notebook.kernel.execute(`request_rubric("${{title}}", "${{description}}","
        " "${{similarTo}}")`);
    }});
    </script>
    """
    display(HTML(form_html))
