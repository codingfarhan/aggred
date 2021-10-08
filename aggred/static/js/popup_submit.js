function close_footer() {
    footer = document.getElementById("footer");

    footer.style.display = "none";
}

function popup_form(action) {
    popup = document.getElementById("popup_form");
    body_tag = document.getElementsByTagName("body")[0];

    // body_tag.style.filter = "blur(8px)";

    popup.style.display = "block";
    popup.style.backdropFilter = "blur(3px)";

    // manipulating form field names as per the action:

    form_heading = document.getElementById("form-heading");
    form_title = document.getElementById("form-title");
    explanation = document.getElementById("explanation");

    form_submit = document.getElementById("form-btn");

    if (action == "ask") {
        form_heading.innerText = "Ask a Question";
        form_title.style.display = "block";
        explanation.innerText = "Explain *";
        form_submit.value = "POST";
        form_submit.textContent = "POST";
    } else if (action == "Answer") {
        form_heading.innerText = "Answer randomUser's question";
        form_title.style.display = "block";
        explanation.innerText = "Explain *";
        form_submit.value = "Answer";
        form_submit.textContent = "Answer";

        document.getElementsByClassName("category-options")[0].style.display =
            "none";
    } else if (action.startsWith("Reply,")) {
        form_heading.innerText = "REPLY";
        form_title.style.display = "none";
        explanation.innerText = "Explain";
        form_submit.value = action;
        form_submit.textContent = "Reply";

        document.getElementsByClassName("category-options")[0].style.display =
            "none";
        document.getElementById("title_row").style.display = "none";
    } else if (action.startsWith("Reply To Answer")) {
        console.log("replying to answer..");
        form_heading.innerText = "REPLY TO ANSWER";
        form_title.style.display = "none";
        explanation.innerText = "Explain *";
        form_submit.value = action;
        form_submit.textContent = "Reply";

        document.getElementsByClassName("category-options")[0].style.display =
            "none";
        document.getElementById("title_row").style.display = "none";
    }
}

function close_popup(id_elem) {
    popup = document.getElementById(id_elem);
    popup.style.display = "none";
}

function redirect_here(name) {
    window.location.pathname = name;
}