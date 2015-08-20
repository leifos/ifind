function validate_required(field) {
    with (field) {
        if (value == null || value == "") {
            return false;
        }
        else {
            return true;
        }
    }
}

function validate_form(thisform) {
    with (thisform) {
        if (validate_required(query) == false) {
            query.focus();
            return false;
        }
    }
}