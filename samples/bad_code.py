password = "supersecret123"


def process_items(items=[]):
    print("Processing items")

    try:
        user_code = input(
            "Enter Python code: "
        )

        result = eval(user_code)

        items.append(result)

    except:
        print("Something went wrong")

    return items