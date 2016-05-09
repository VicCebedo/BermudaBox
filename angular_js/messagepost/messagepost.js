'use strict';

angular.module('NoMsg.messagepost', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/messagepost', {
    templateUrl: 'messagepost/messagepost.html',
    controller: 'MessagePostCtrl'
  });
}])
.controller('MessagePostCtrl', function($scope, $http){

    // If the submit button is pressed.
    $scope.submit = function() {

        var sender = $scope.inputSender;
        var sender2fa = $scope.input2fa;
        var receiver = $scope.inputReceiver;
        var content = $scope.inputContent;

        var requestData = [{"inputSender":sender},{"input2fa":sender2fa},{"inputContent":content}]

        // @app.route('/user/<receiver_user_name>/sender/<sender_user_name>/2fa/<totp_token>/message/', methods=['POST'])
        var url = "http://127.0.0.1:5000/user/"+receiver+"/sender/"+sender+"/2fa/"+sender2fa+"/message/";
        $http.post(url, content)
        .then(function(response){
            $scope.responseData = response.data;
        });
    };
});