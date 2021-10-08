select_post1 = document.getElementById("post_class");
select_post2 = document.getElementById("post_subject_or_course");

for (var i = 1; i <= 12; i++) {
    new_option = document.createElement("option");

    option_value = `Class ${i}`;
    new_option.value = option_value;
    new_option.innerText = option_value;

    select_post1.appendChild(new_option);
}

/* set value of next datalist element as: "Maths", "Science", etc */

subject_list = [
    "English",
    "Hindi",
    "Urdu",
    "Sanskrit",
    "Punjabi",
    "Bengali",
    "Tamil",
    "Telugu",
    "Sindhi",
    "Marathi",
    "Gujarati",
    "Manipuri",
    "Malayalam",
    "Odia",
    "Assamese",
    "Kannada",
    "Arabic",
    "Tibetan",
    "French",
    "German",
    "Russian",
    "Persian",
    "Nepali",
    "Limboo",
    "Lepcha",
    "Telugu Telangana",
    "BODO",
    "Tangkhul",
    "Japanese",
    "Bhutia",
    "Spanish",
    "Kashmiri",
    "Mizo",
    "Bahasa Melayu",
    "History",
    "Political Science",
    "Geography",
    "Economics",
    "Carnatic Music",
    "Hindustani Music",
    "Psychology",
    "Sociology",
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "Biotechnology",
    "Physical Education",
    "Painting",
    "Sculpture",
    "Art",
    "Business Studies",
    "Accountancy",
    "Dance",
    "Home Science",
    "Informatics Practices",
    "Computer Science",
    "Entrepreneurship",
    "National Caded Corps (NCC)",
    "Information Technology",
    "Agriculture",
    "Marketing",
    "Yoga",
    "Fashion",
    "Artificial Intelligence",
    "Media",
    "Banking",
];

for (subject in subject_list) {
    new_option = document.createElement("option");

    option_value = subject_list[subject];
    new_option.value = option_value;
    new_option.innerText = option_value;

    select_post2.appendChild(new_option);
}