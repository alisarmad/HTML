function validateEmail(sEmail) 
{
  var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
  if (filter.test(sEmail)) 
  {
      return true;
  }
  else 
  {
      return false;
  }
}

// $(document).on('click','#close_reload',function(e){  
//       location.reload(true);
// });


// $(document).on('click','#close_reload_symbol',function(e){  
//       location.reload(true);
// });

$(document).ready(function () {
   $('input[type=text]').on('keypress', function(e) {
      if (e.which == 32)
      {
        console.log('no space')
        return false;
      }
  });
});

$(document).ready(function () {
$('#password').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });
});

$(document).on('click','#entrepreneurs_sign_up_btn',function(e){
 console.log("Hello !!")  
var user_type = $('#user_type').val();
var first_name = $('#first_name').val();
var surname = $('#surname').val();
var email = $('#email').val();
var password = $('#password').val();
var date_of_birth = $('#date_of_birth').val();
var position_in_company = $('#position_in_company').val();
var working_years = $('#working_years').val();
var no_of_employees = $('#no_of_employees').val();
var website_url = $('#website_url').val();
var company_registration_number = $('#company_registration_number').val();
var address = $('#address').val();
var skills_interested = $('#skills_interested option:selected').val();
var industry_interested = $('#industry_interested option:selected').val();
var country =$('#country option:selected').val();
var token=$('input[name="csrfmiddlewaretoken"]').val();
var phone_number = $('#phone_number').val();
  first_name = first_name.trim()
  surname = surname.trim()
  date_of_birth = date_of_birth.trim()
  email = email.trim()
  address = address.trim()
  website_url = website_url.trim()

 if(first_name.length == 0)
 {
    alert('First_name is required');
    return false;
 }
 else
 {
   if (first_name.match(/^[a-zA-Z\s]+$/))
     {
       first_name = first_name.replace(/  +/g, ' '); 
       console.log('name done.')
       // alert('valid');  
     }
   else
     {
       // alert('invalid')
       alert('Only alphabets are allowed for this field.');
       return false;
     }

   
 }

  if(first_name.length > 25)
  {

    alert('Max length of Name is 25.');
    return false;

  }
  if(first_name.length > 0 && first_name.length <= 25)
  {
    console.log(' name done.')
  }


 if(email.length == 0)
  {
    alert('Email is required.');
     return false;
  }
  else
  {
    if(validateEmail(email))
    {
      console.log('valid email');
    }
    else
    {
      alert('Enter valid email.');
       return false;
    }
  }


  if(password.length == 0)
  {
      alert('Password is required.');
     return false;
  }

  if(password.length > 7)
  {
    console.log('done.')
   }
   else
  {
    alert('Min length of password is 8.');
    return false;
  }


  console.log("before ajax")
  $.ajax({
    url: '/entrepreneurs_registration/',
    type: "POST",
    data: {'user_type':user_type,'first_name':first_name,'surname':surname,'email':email,'password':password,'date_of_birth':date_of_birth,'position_in_company':position_in_company,'working_years':working_years,'no_of_employees':no_of_employees,'website_url':website_url,'company_registration_number':company_registration_number,'address':address,'skills_interested':skills_interested,'industry_interested':industry_interested,'country':country,'phone_number':phone_number,'csrfmiddlewaretoken':token },
    dataType: 'json',
    cache: false,
    success: function(response){
     // if(response == '3')
     //  {
     //    // alert('Email already registered.');
     //    $("#email_txt").text('Email already registered.');
     //    document.getElementById("email_txt").style.color = "red";
     //    return false;
     //  }
     
        
     if(response=='1')
      {
        console.log(response)
        alert("Registration done.");
        // $('#info_model').modal('show');
        // $("#p_text").text("Registration done.");
        window.location.href='/login/';
      }
      else
      {
        if(response=='0')
        {
          alert('This Email is already registered.');
          console.log(response)
          console.log('done.')
          // $("#email_txt").text('E-mail already registered.');
          // document.getElementById("email_txt").style.color = "red";
          return false;
        }       
      }
    }
  });
});


$(document).ready(function () {
  $('#confirm_password').keypress(function (e) {
    if (e.keyCode == 13)
    {
      $('#confirm_password').click();
    }
  });
});






