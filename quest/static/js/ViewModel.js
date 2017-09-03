function ViewModel() {
    var self = this;

    self.id = undefined;
    self.title = ko.observable();
    self.description = ko.observable();
    self.client = ko.observable();
    self.priority = ko.observable();
    self.target_date = ko.observable();
    self.product_area = ko.observable();

    self.resetFields = function () {
        self.id = undefined;
        self.title("");
        self.description("");
        self.client("A");
        self.priority(1);
        self.target_date("2017-09-03");
        self.product_area("billing");
    };

    self.resetFields();

    self.isNew = ko.computed(function () {
        return self.id === undefined;
    });

    self.isValid = ko.computed(function () {
        return self.title().length > 0
            && self.description().length > 0
            && clientIsValid(self.client())
            && self.priority() > 0
            && dateIsValid(self.target_date())
            && productAreaIsValid(self.product_area());
    });

    self.featureRequests = ko.observableArray();
    self.loading = ko.observable(false);

    self.loadFeatureRequests = function () {
        self.loading(true);
        ajax({
            method: "GET",
            url: "/api/features",
        }, function (data) {
            self.loading(false);
            self.featureRequests(data.features);
        });
    };

    self.savePendingFeatureRequest = function () {
        var data = JSON.stringify({
            title: self.title(),
            description: self.description(),
            client: self.client(),
            priority: self.priority(),
            target_date: self.target_date(),
            product_area: self.product_area(),
        });

        ajax({
            method: "POST",
            url: "/api/features",
            data: data,
        }, function (data) {
            self.resetFields();
            self.loadFeatureRequests();
        });
    };
}

function ajax(params, callback) {
    params.contentType = "application/json";
    params.dataType = "json";
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

var DATE_REGEX = /\d{4}-\d{2}-\d{2}/;

function dateIsValid(date) {
    return DATE_REGEX.test(date);
}

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
