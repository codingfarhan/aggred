window.onload = function() {
    // important variables:

    userEmail = JSON.parse(document.getElementById("userEmail").textContent);

    // initial state of like and save icons:

    initial_icons = JSON.parse(
        document.getElementById("initial_icons").textContent
    );

    console.log(initial_icons);

    // console.log(`liked: ${typeof liked}, saved: ${saved}`);

    function setInitialIconState(initial_icons) {
        for (var i = 0; i < initial_icons.length; i++) {
            document.getElementById(initial_icons[i]).style.display = "block";

            if (initial_icons[i].startsWith("like") == true) {
                document.getElementById(
                    initial_icons[i].replace("like", "dislike")
                ).style.display = "none";
            }

            if (initial_icons[i].startsWith("dislike") == true) {
                document.getElementById(
                    initial_icons[i].replace("dislike", "like")
                ).style.display = "none";
            }

            if (initial_icons[i].startsWith("save") == true) {
                document.getElementById(
                    initial_icons[i].replace("save", "unsave")
                ).style.display = "none";
            }

            if (initial_icons[i].startsWith("unsave") == true) {
                document.getElementById(
                    initial_icons[i].replace("unsave", "save")
                ).style.display = "none";
            }
        }
    }

    // important element ID:

    like_icon = "like-icon";
    dislike_icon = "dislike-icon";

    save_icon = "save-icon";
    unsave_icon = "unsave-icon";

    // calling function to set initial state of icons for the post:

    setInitialIconState(initial_icons);

    // Event listeners calling AJAX functions:

    like_elems = document.getElementsByClassName("like-icon");

    // console.log(like_elems[0].id);

    for (var i = 0; i < like_elems.length; i++) {
        // console.log(like_elems[i].id);
        like_id_ = like_elems[i].id;
        document.getElementById(like_id_).addEventListener("click", function() {
            ajax_operation(like_id_);
        });
    }

    dislike_elems = document.getElementsByClassName("dislike-icon");

    for (var i = 0; i < dislike_elems.length; i++) {
        dislike_id_ = dislike_elems[i].id;
        document.getElementById(dislike_id_).addEventListener("click", function() {
            ajax_operation(dislike_id_);
        });
    }

    save_elems = document.getElementsByClassName("save-icon");

    for (var i = 0; i < save_elems.length; i++) {
        save_id_ = save_elems[i].id;
        document.getElementById(save_id_).addEventListener("click", function() {
            ajax_operation(save_id_);
        });
    }

    unsave_elems = document.getElementsByClassName("unsave-icon");

    for (var i = 0; i < unsave_elems.length; i++) {
        unsave_id_ = unsave_elems[i].id;
        document.getElementById(unsave_id_).addEventListener("click", function() {
            ajax_operation(unsave_id_);
        });
    }

    // DOM manipulation function:

    function dom_manipulation(clicked_icon) {
        // when liking a post:
        if (clicked_icon.startsWith("like,") == true) {
            document.getElementById(clicked_icon).style.display = "none";

            document.getElementById(
                clicked_icon.replace("like", "dislike")
            ).style.display = "block";

            // updating likes:

            target_elem = document.getElementById(
                clicked_icon.replace("like", "likes")
            );
            current_likes = parseInt(target_elem.textContent);

            current_likes += 1;

            target_elem.textContent = `${current_likes} Likes`;
        }

        // when disliking a post:
        if (clicked_icon.startsWith("dislike,") == true) {
            document.getElementById(clicked_icon).style.display = "none";

            document.getElementById(
                clicked_icon.replace("dislike", "like")
            ).style.display = "block";

            // updating likes:

            target_elem = document.getElementById(
                clicked_icon.replace("dislike", "likes")
            );
            current_likes = parseInt(target_elem.textContent);

            current_likes -= 1;

            target_elem.textContent = `${current_likes} Likes`;
        }

        // when saving a post:
        if (clicked_icon.startsWith("save,") == true) {
            document.getElementById(clicked_icon).style.display = "none";

            document.getElementById(
                clicked_icon.replace("save", "unsave")
            ).style.display = "block";
        }

        // when unsaving a post:
        if (clicked_icon.startsWith("unsave,") == true) {
            document.getElementById(clicked_icon).style.display = "none";

            document.getElementById(
                clicked_icon.replace("unsave", "save")
            ).style.display = "block";
        }
    }

    // AJAX code to send/receive data:

    function ajax_operation(element_id) {
        console.log("Executing AJAX");

        console.log(`element_id= ${element_id}`);
        // Establishing connection with url:

        var xhr = new XMLHttpRequest();

        xhr.open("POST", `/ajax/like_save_vote/`, true);

        csrftoken = document.cookie.split(";")[2].split("=")[1];

        // console.log(csrftoken);

        xhr.setRequestHeader("Content-type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrftoken);

        if (xhr.readyState == 0) {
            console.log("COnnecting to url...");
        }

        if (xhr.readyState == 1) {
            console.log("CONNECTED!!");

            // if liking a post:

            if (element_id.startsWith("like,") == true) {
                post_id = element_id.split(",")[1];
                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "like",
                    })
                );
            }

            // if disliking a post:
            else if (element_id.startsWith("dislike,") == true) {
                post_id = element_id.split(",")[1];

                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "dislike",
                    })
                );
            }

            // if saving a post:
            else if (element_id.startsWith("save,") == true) {
                post_id = element_id.split(",")[1];

                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "save",
                    })
                );
            }

            // if unsaving a post:
            else if (element_id.startsWith("unsave,") == true) {
                post_id = element_id.split(",")[1];

                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "unsave",
                    })
                );
            }

            // Manipulating the DOM as per element_id:

            if (element_id.startsWith("like,") == true) {
                dom_manipulation(element_id);
            } else if (element_id.startsWith("dislike,") == true) {
                dom_manipulation(element_id);
            } else if (element_id.startsWith("save,") == true) {
                dom_manipulation(element_id);
            } else if (element_id.startsWith("unsave,") == true) {
                dom_manipulation(element_id);
            }
        }

        // Connection updates on the browser's console:

        if (xhr.readyState == 2) {
            console.log("WS connection closing..");
        }

        if (xhr.readyState == 3) {
            console.log("WS connection closed..");
        }
    }
};