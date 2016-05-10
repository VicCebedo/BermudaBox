'use strict';

angular.module('NoMsg.messagegetall', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/messagegetall', {
    templateUrl: 'messagegetall/messagegetall.html',
    controller: 'InboxCtrl'
  });
}])
.controller('InboxCtrl', function($scope, $http){

    // If the delete button is pressed.
    $scope.delete = function(messageID) {
        var user2fa = $scope.input2fa;
        var username = $scope.inputUsername;

        // @app.route('/user/<user_name>/2fa/<totp_token>/message/<message_id>', methods=['DELETE'])
        var url = "http://127.0.0.1:5000/user/"+username+"/2fa/"+user2fa+"/message/"+messageID;
        $http.delete(url)
        .then(function(response){
            var responseData = response.data;
            $scope.responseText = responseData;
            $scope.responseData = "";
        });
    };

    // If the delete all button is pressed.
    $scope.deleteAll = function() {
        var user2fa = $scope.input2fa;
        var username = $scope.inputUsername;

        // @app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['DELETE'])
        var url = "http://127.0.0.1:5000/user/"+username+"/2fa/"+user2fa+"/message/";
        $http.delete(url)
        .then(function(response){
            var responseData = response.data;
            $scope.responseText = responseData;
            $scope.responseData = "";
        });
    };

    // If the submit button is pressed.
    $scope.submit = function() {

        var user2fa = $scope.input2fa;
        var username = $scope.inputUsername;

        // @app.route('/user/<user_name>/2fa/<totp_token>/message/', methods=['GET'])
        var url = "http://127.0.0.1:5000/user/"+username+"/2fa/"+user2fa+"/message/";
        $http.get(url)
        .then(function(response){
            var responseData = response.data;

            // If response was error,
            // display the text rather than displaying the table.
            if(responseData.indexOf("Error:") == -1){
                $scope.responseText = "";
                $scope.responseData = responseData;
            } else {
                $scope.responseText = responseData;
            }
        });
    };
});