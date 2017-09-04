// steal the current date from the template
var currentDate = $("#input-date").attr("min");

function ViewModel() {
    // mmm love that dynamic binding workaround
    var self = this;

    // app data
    self.featureRequests = ko.observableArray();
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
        self.title("");
        self.description("");
        self.client("A");
        self.priority(1);
        self.target_date(currentDate);
        self.product_area("billing");
    };

    // keepin' it DRY
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
            url: "/api/features",
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
            url: "/api/features/" + featureRequest.id,
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

var PRODUCT_AREA_NAMES = {
    policies: "Policies",
    billing: "Billing",
    claims: "Claims",
    reports: "Reports",
};

var PRODUCT_AREA_CLASSES = {
    policies: "panel-success",
    billing: "panel-info",
    claims: "panel-warning",
    // everyone knows reports are the most dangerous
    reports: "panel-danger",
};
