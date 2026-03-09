def remove_duplicates(tools):

    seen = set()
    unique_tools = []

    for tool in tools:

        name = tool.get("name")

        if name and name not in seen:

            unique_tools.append(tool)
            seen.add(name)

    return unique_tools