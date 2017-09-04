function ajax(params, callback) {
    params.contentType = "application/json";
    params.dataType = params.method !== "DELETE" && "json";
    params.success = callback;
    params.error = function (xhr, status, message) {
        displayErrorMessage(message);
    };

    return $.ajax(params);
}

function displayErrorMessage(message) {
    var text = "Error: " + message;
    alert(text);
}
