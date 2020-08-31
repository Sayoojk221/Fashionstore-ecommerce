$(document).ready(function(){
    $('#email-reg').change(function(){
        var email = $('#email-reg').val()
        $.ajax({
            url:'/emailpasswordcheck/',
            data:{
                'email':email,
            },
            success:function(item){
                $('#error').html(item.emailid)
            }
        });
    })
    $('#phone-reg').change(function(){
        var phone = $('#phone-reg').val()
        $.ajax({
            url:'/emailpasswordcheck/',
            data:{
                'phone':phone
            },
            success:function(item){
                $('#error').html(item.phoneno)
            }
        });
    })
    $('#email-log').change(function(){
        var email = $('#email-log').val()
        $.ajax({
            url:'/emailpasswordchecklogin/',
            data:{
                'email':email
            },
            success:function(item){
                $('#error').html(item.email)
            }
        });
    })
    $('#pass-log').change(function(){
        var pass = $('#pass-log').val()
        var email = $('#email-log').val()
        $.ajax({
            url:'/emailpasswordchecklogin/',
            data:{
                'email':email,
                'password':pass
            },
            success:function(item){
                $('#error').html(item.password)
            }
        });
    })

})
