'use strict';

angular.module('NoMsg.messagepostanon', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/messagepostanon', {
    templateUrl: 'messagepostanon/messagepostanon.html',
    controller: 'MessagePostAnonCtrl'
  });
}])
.controller('MessagePostAnonCtrl', function($scope, $http){

    // If the submit button is pressed.
    $scope.submit = function() {

        var receiver = $scope.inputReceiver;
        var content = $scope.inputContent;

        // @app.route('/user/<receiver_user_name>/sender/anon/message/', methods=['POST'])
        var url = "http://127.0.0.1:5000/user/"+receiver+"/sender/anon/message/";
        $http.post(url, content)
        .then(function(response){
            $scope.responseData = response.data;
        });
    };
});