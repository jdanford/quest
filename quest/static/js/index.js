var viewModel = new ViewModel();
viewModel.loadFeatureRequests(function () {
    ko.applyBindings(viewModel);
});
