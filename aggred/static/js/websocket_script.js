window.onload = function() {
    // initial state of like and save icons:

    liked = JSON.parse(document.getElementById("liked").textContent);
    saved = JSON.parse(document.getElementById("saved").textContent);

    function setInitialIconState(liked, saved) {
        if (liked == "True") {
            document.getElementById(like_icon).style.display = "block";
        } else {
            document.getElementById(dislike_icon).style.display = "block";
        }

        if (saved == "True") {
            document.getElementById(save_icon).style.display = "block";
        } else {
            document.getElementById(unsave_icon).style.display = "block";
        }
    }

    // important element ID:

    like_icon = "like-icon";
    dislike_icon = "dislike-icon";

    save_icon = "save-icon";
    unsave_icon = "unsave-icon";

    // calling function to set initial state of icons for the post:

    setInitialIconState(liked, saved);

    // Backend data:

    post_id = JSON.parse(document.getElementById("post_id").textContent);

    userEmail = JSON.parse(document.getElementById("userEmail").textContent);

    // Event listeners calling websocket functions:

    document
        .getElementById(like_icon)
        .addEventListener("click", websocket_operation(like_icon));
    document
        .getElementById(dislike_icon)
        .addEventListener("click", websocket_operation(dislike_icon));
    document
        .getElementById(save_icon)
        .addEventListener("click", websocket_operation(save_icon));
    document
        .getElementById(unsave_icon)
        .addEventListener("click", websocket_operation(unsave_icon));

    // DOM manipulation function:

    function dom_manipulation(clicked_icon) {
        // when liking a post:
        if (clicked_icon == like_icon) {
            document.getElementById(like_icon).style.display = "none";

            document.getElementById(dislike_icon).style.display = "block";
        }

        // when disliking a post:
        if (clicked_icon == dislike_icon) {
            document.getElementById(dislike_icon).style.display = "none";

            document.getElementById(like_icon).style.display = "block";
        }

        // when liking a post:
        if (clicked_icon == save_icon) {
            document.getElementById(save_icon).style.display = "none";

            document.getElementById(unsave_icon).style.display = "block";
        }

        // when liking a post:
        if (clicked_icon == unsave_icon) {
            document.getElementById(unsave_icon).style.display = "none";

            document.getElementById(save_icon).style.display = "block";
        }
    }

    // Websocket function communicating with Backend:

    function websocket_operation(element_id) {
        // Establishing Websocket Connection first:

        var ws = new WebSocket(
            "wss://" +
            window.location.host +
            "/ws/interact_with_post/" +
            post_id +
            "/"
        );

        if (ws.readyState == 1) {
            console.log("WEBSOCKET CONNECTED!!");

            // if liking a post:

            if (element_id == like_icon) {
                ws.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "like",
                    })
                );
            }

            // if disliking a post:
            else if (element_id == dislike_icon) {
                ws.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "dislike",
                    })
                );
            }

            // if saving a post:
            else if (element_id == save_icon) {
                ws.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "save",
                    })
                );
            }

            // if unsaving a post:
            else if (element_id == unsave_icon) {
                ws.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "unsave",
                    })
                );
            }

            ws.onmessage = function(e) {
                received_data = JSON.parse(e.data);

                console.log(received_data["message"]);

                if (received_data["action"] == "like") {
                    dom_manipulation(like_icon);
                } else if (received_data["action"] == "dislike") {
                    dom_manipulation(dislike_icon);
                } else if (received_data["action"] == "save") {
                    dom_manipulation(save_icon);
                } else if (received_data["action"] == "unsave") {
                    dom_manipulation(unsave_icon);
                }
            };
        }
    }
};