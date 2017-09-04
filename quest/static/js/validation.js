function dateIsValid(date) {
    return DATE_REGEX.test(date);
}

var DATE_REGEX = /\d{4}-\d{2}-\d{2}/;

function clientIsValid(client) {
    return !!VALID_CLIENTS[client];
}

var VALID_CLIENTS = {
    A: true,
    B: true,
    C: true,
};

function productAreaIsValid(productArea) {
    return !!VALID_PRODUCT_AREAS[productArea];
}

var VALID_PRODUCT_AREAS = {
    policies: true,
    billing: true,
    claims: true,
    reports: true,
};
