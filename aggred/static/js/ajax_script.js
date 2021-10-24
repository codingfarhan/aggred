window.onload = function() {
    // initial state of like and save icons:

    liked = JSON.parse(document.getElementById("liked").textContent);
    saved = JSON.parse(document.getElementById("saved").textContent);

    // console.log(`liked: ${typeof liked}, saved: ${saved}`);

    function setInitialIconState(liked, saved) {
        if (liked == true) {
            document.getElementById(like_icon).style.display = "none";
            document.getElementById(dislike_icon).style.display = "block";
        } else {
            document.getElementById(dislike_icon).style.display = "none";
            document.getElementById(like_icon).style.display = "block";
        }

        if (saved == true) {
            document.getElementById(save_icon).style.display = "none";
            document.getElementById(unsave_icon).style.display = "block";
        } else {
            document.getElementById(unsave_icon).style.display = "none";
            document.getElementById(save_icon).style.display = "block";
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

    // Event listeners calling AJAX functions:

    document.getElementById(like_icon).addEventListener("click", function() {
        ajax_operation(like_icon);
    });
    document.getElementById(dislike_icon).addEventListener("click", function() {
        ajax_operation(dislike_icon);
    });
    document.getElementById(save_icon).addEventListener("click", function() {
        ajax_operation(save_icon);
    });
    document.getElementById(unsave_icon).addEventListener("click", function() {
        ajax_operation(unsave_icon);
    });

    // DOM manipulation function:

    function dom_manipulation(clicked_icon) {
        // when liking a post:
        if (clicked_icon == like_icon) {
            document.getElementById(like_icon).style.display = "none";

            document.getElementById(dislike_icon).style.display = "block";

            // updating likes:

            target_elem = document.getElementById(`likes-${post_id}`);
            current_likes = parseInt(target_elem.textContent);

            current_likes += 1;

            target_elem.textContent = `${current_likes} Likes`;
        }

        // when disliking a post:
        if (clicked_icon == dislike_icon) {
            document.getElementById(dislike_icon).style.display = "none";

            document.getElementById(like_icon).style.display = "block";

            // updating likes:

            target_elem = document.getElementById(`likes-${post_id}`);
            current_likes = parseInt(target_elem.textContent);

            current_likes -= 1;

            target_elem.textContent = `${current_likes} Likes`;
        }

        // when saving a post:
        if (clicked_icon == save_icon) {
            document.getElementById(save_icon).style.display = "none";

            document.getElementById(unsave_icon).style.display = "block";
        }

        // when unsaving a post:
        if (clicked_icon == unsave_icon) {
            document.getElementById(unsave_icon).style.display = "none";

            document.getElementById(save_icon).style.display = "block";
        }
    }

    // AJAX code to send/receive data:

    function ajax_operation(element_id, action, answerID) {
        console.log("Executing AJAX");
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

            if (element_id == like_icon) {
                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "like",
                    })
                );
            }

            // if disliking a post:
            else if (element_id == dislike_icon) {
                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "dislike",
                    })
                );
            }

            // if saving a post:
            else if (element_id == save_icon) {
                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "save",
                    })
                );
            }

            // if unsaving a post:
            else if (element_id == unsave_icon) {
                xhr.send(
                    JSON.stringify({
                        userEmail: userEmail,
                        post_id: post_id,
                        action: "unsave",
                    })
                );
            }

            // Manipulating the DOM as per element_id:

            if (element_id == like_icon) {
                dom_manipulation(like_icon);
            } else if (element_id == dislike_icon) {
                dom_manipulation(dislike_icon);
            } else if (element_id == save_icon) {
                dom_manipulation(save_icon);
            } else if (element_id == unsave_icon) {
                dom_manipulation(unsave_icon);
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