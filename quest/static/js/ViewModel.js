function ViewModel() {
    // mmm love that dynamic binding workaround
    var self = this;

    // app data
    self.featureRequests = ko.observableArray();
    self.activeClient = ko.observable("");
    self.loading = ko.observable(false);

    // editor fields
    self.id = undefined;
    self.title = ko.observable();
    self.description = ko.observable();
    self.client = ko.observable();
    self.priority = ko.observable();
    self.target_date = ko.observable();
    self.product_area = ko.observable();

    self.resetFields = function () {
        self.id = undefined;
        self.title(FIELD_DEFAULTS.title);
        self.description(FIELD_DEFAULTS.description);
        self.priority(FIELD_DEFAULTS.priority);
        self.target_date(FIELD_DEFAULTS.target_date);
        self.product_area(FIELD_DEFAULTS.product_area);
        self.resetClientField();
    };

    self.resetClientField = function (client) {
        self.client(client || self.activeClient() || FIELD_DEFAULTS.client);
    };

    // keep it DRY
    self.resetFields();

    // keep the client field synced up with the active client
    self.activeClient.subscribe(self.resetClientField);

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

    self.setActiveClient = function (client) {
        self.activeClient(client);
    };

    self.activeClientName = ko.computed(function () {
        return ACTIVE_CLIENT_NAMES[self.activeClient()];
    });

    self.filteredFeatureRequests = ko.computed(function () {
        var client = self.activeClient();
        return self.featureRequests().filter(function (featureRequest) {
            return !client || featureRequest.client === client;
        });
    });

    self.loadFeatureRequests = function (callback) {
        self.loading(true);
        ajax({
            method: "GET",
            url: API_PREFIX + "/features",
        }, function (data) {
            self.loading(false);
            self.featureRequests(data.features);
            callback && callback();
        });
    };

    self.savePendingFeatureRequest = function () {
        // this could be shorter if `ko.toJSON()` accepted a list of keys
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
            url: API_PREFIX + "/features",
            data: data,
        }, function (data) {
            self.resetFields();
            self.loadFeatureRequests();
        });
    };

    self.deleteFeatureRequest = function (featureRequest) {
        var message = "Are you sure you want to delete \"" + featureRequest.title + "\"?";
        if (!confirm(message)) {
            return;
        }

        ajax({
            method: "DELETE",
            url: API_PREFIX + "/features/" + featureRequest.id,
        }, function (data) {
            self.loadFeatureRequests();
        });
    };

    self.productAreaName = function (productArea) {
        return PRODUCT_AREA_NAMES[productArea];
    };

    self.featureRequestClass = function (featureRequest) {
        return PRODUCT_AREA_CLASSES[featureRequest.product_area];
    };
}

var API_PREFIX = "/api";

// steal the current date from the template
var currentDate = $("#input-date").attr("min");

var FIELD_DEFAULTS = {
    title: "",
    description: "",
    priority: 1,
    target_date: currentDate,
    product_area: "policies",
    client: "A",
};

var ACTIVE_CLIENT_NAMES = {
    "": "all clients",
    A: "Client A",
    B: "Client B",
    C: "Client C",
}

var PRODUCT_AREA_NAMES = {
    policies: "Policies",
    billing: "Billing",
    claims: "Claims",
    reports: "Reports",
};

var PRODUCT_AREA_CLASSES = {
    policies: "panel-info",
    billing: "panel-success",
    claims: "panel-warning",
    // everyone knows reports are the most dangerous
    reports: "panel-danger",
};
