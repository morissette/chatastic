/*
 * Handle scroll fixed from bottom to top
 */
$(window).scroll(function () {
  var mn = $(".nav-login");
  var viewportHeight = $(window).height();

  if( $(this).scrollTop() > viewportHeight ) {
    mn.addClass("fixed-to-top");
  } else {
    mn.removeClass("fixed-to-top");
  }
});

var api_url = 'http://127.0.0.1:5000';

(function() {
  var app = angular.module('chatastic', ['ngRoute']);

  /*
   * Handle application frontend routing
   */
  app.config(function($routeProvider, $locationProvider) {
    $routeProvider.
        when('/dashboard', {
          templateUrl: 'partials/dashboard.html',
          controller: 'dashboardCtrl',
          currentPage: 'Dashboard'
        }).
        when('/settings', {
          templateUrl: 'partials/settings.html',
          controller: 'settingsCtrl',
          currentPage: 'Settings'
        }).
        when('/pagerduty/settings', {
          templateUrl: 'partials/pagerduty.html',
          controller: 'pagerdutyCtrl',
          currentPage: 'Pagerduty Settings'
        }).
        when('/slack/settings', {
          templateUrl: 'partials/slack.html',
          controller: 'slackCtrl',
          currentPage: 'Slack Settings'
        }).
        when('/hipchat/settings', {
       	  templateUrl: 'partials/hipchat.html',
          controller: 'hipchatCtrl',
          currentPage: 'HipChat Settings' 
        }).
        when('/victorops/settings', {
		  templateUrl: 'partials/victorops.html',
          controller: 'victoropsCtrl',
          currentPage: 'VictorOps Settings'
        }).
        when('/opsgenie/settings', {
		  templateUrl: 'partials/opsgenie.html',
          controller: 'opsgenieCtrl',
          currentPage: 'OpsGenie Settings'
        }).
        when('/alertops/settings', {
		  templateUrl: 'partials/alertops.html',
          controller: 'alertopsCtrl',
          currentPage: 'AlertOps Settings'
        }).
        otherwise({
          redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
  });

  app.run(function ($rootScope, $route) {
    $rootScope.$on("$routeChangeSuccess", function(currentRoute, previousRoute) {
      $rootScope.currentPage = $route.current.currentPage;

      /*
       * Handle logout all hacky like
       */
      if (!$route.current.currentPage) {
        $rootScope.loggedIn = false;
      }
    });
  });

  /*
   * Controller Over <body>
   */
  app.controller("bodyCtrl", function($scope) {
    // shouldn't use such a huge controller
  });

  /*
   * Handle User Login
   */
  app.controller("loginCtrl", function($scope, $rootScope, $location, $http) {
    var vm = $scope;
    vm.user = {};

    vm.signIn = function() {
      var email = vm.user.email;
      var password = vm.user.password;
      if ( email && password ) {
        vm.success = true;
        $rootScope.loggedIn = true;
        $location.path('/dashboard');
      } else {
        vm.error = "Missing required fields";
      }
    };

  });

  /*
   * Dashboard CTRL
   */
  app.controller('dashboardCtrl', function($scope, $rootScope) {
    $rootScope.loggedIn = true;
  });

  /*
   * Header directive
   */
  app.directive('dashboardHeader', function() {
      return {
          restrict: 'E',
          templateUrl: 'partials/header.html'
      };
  });

  /*
   * Settings CTRL
   */
  app.controller('settingsCtrl', function($scope) {

  });

  app.controller('pagerdutyCtrl', function($scope) {

  });

  app.controller('slackCtrl', function($scope) {

  });

  app.controller('hipchatCtrl', function($scope) {

  });

  app.controller('victoropsCtrl', function($scope) {

  });

  app.controller('opsgenieCtrl', function($scope) {

  });

  app.controller('alertopsCtrl', function($scope) {

  });

})();
