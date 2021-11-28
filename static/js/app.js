function getmodeldata(regno){
    $.ajax(
    {
        type:"GET",
        url: "",
        data:{ getmodeldata:'True',regno: regno },
        dataType: 'json',
        success: function( data ) 
    {

        output = JSON.parse(data)
        document.getElementById("modelregnotitle").innerHTML = output[0].fields.Reg_No;
        document.getElementById("modelregno").innerHTML = output[0].fields.Reg_No;
        document.getElementById("modelrollno").innerHTML = output[0].fields.Roll_No;
        document.getElementById("modelname").innerHTML = output[0].fields.Name;
        document.getElementById("modeldob").innerHTML = output[0].fields.DOB;
        document.getElementById("modeldept").innerHTML = output[0].fields.Dept;
        document.getElementById("modelyear").innerHTML = output[0].fields.Year;
        document.getElementById("modelemail").innerHTML = output[0].fields.Email;
        document.getElementById("modelfather").innerHTML = output[0].fields.Father_Name;
        document.getElementById("modeladdress").innerHTML = output[0].fields.Address;
        document.getElementById("modelcommunity").innerHTML = output[0].fields.Caste_Community;
        document.getElementById("modelreligion").innerHTML = output[0].fields.Religion;
        document.getElementById("modeldoa").innerHTML = output[0].fields.Date_Of_Admission;
        document.getElementById("modelconduct").innerHTML = output[0].fields.Conduct;
    }
    })
    $.ajax(
        {
            type:"GET",
            url: "",
            data:{ getmodeldatadue:'True',regno: regno },
            dataType: 'json',
            success: function( data ) 
        {
    
            output = JSON.parse(data)
            index = []
            state = ""
            for(x in output){
                index.push(x)
            }
            for(let i=0; i<index.length; i++){

                if (output[i].is_Done){
                    state = "<div class='nk-tb-col'><span class='badge badge-dot badge-success'>Returned</span></div>"
                } else {
                    state = "<div class='nk-tb-col'><span class='badge badge-dot badge-warning'>Not Returned</span></div>"
                }

                document.getElementById("modeldue").innerHTML += "<div class='nk-tb-item' ><div class='nk-tb-col'><span class='tb-lead'><a href='#'>" + output[i].Dept + "</a></span></div>" + state + "</div>";

            }
            
        }
        })
};

function removedue(regno,dept){
    $.ajax(
        {
            type:"POST",
            url: "",
            data:{ removedue:'True',regno: regno, dept:dept, csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function( data ) 
        {
            $("#nk-block").load(location.href + " #nk-block");
        }
        })
};

function AcceptReq(regno,dept){
    $.ajax(
        {
            type:"POST",
            url: "",
            data:{ AcceptReq:'True',regno: regno, dept:dept, csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function( data ) 
        {
            $("#nk-block").load(location.href + " #nk-block");
        }
        })
};

$('#AddDue').on('submit', function(event){
    event.preventDefault();
    console.log('hit adddue')
    $.ajax(
        {
            type:"POST",
            url: "",
            data : { regno : $('#AddDueRegno').val(), dept : $('#AddDueDept').val(), year : $('#AddDueYear').val(), due : $('#AddDueStatus').val(),  AddDue:'True', csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function( data ) 
        {
            $("#nk-block").load(location.href + " #nk-block");
        }
        })
});

$('#search').on('submit', function(event){
    event.preventDefault();
    console.log('hit search')
    $.ajax(
        {
            type:"GET",
            url: "",
            data : { query : $('#searchquery').val(),search:'True' },
            dataType: 'json',
            success: function( data ) 
        {
            output = JSON.parse(data)
            document.getElementById("searchregno").innerHTML = output[0].fields.Reg_No;
            document.getElementById("searchfirst").innerHTML = output[0].fields.First;
            document.getElementById("searchname").innerHTML = output[0].fields.Name;
            document.getElementById("searchrollno").innerHTML = output[0].fields.Roll_No;
            document.getElementById("searchemail").innerHTML = output[0].fields.Email;
            document.getElementById("searchphone").innerHTML = output[0].fields.Phone;
        }
        })
});

$('#apply').on('submit', function(event){
    event.preventDefault();
    console.log('hit apply')
    $.ajax(
        {
            type:"POST",
            url: "",
            data : { reason : $('#purpose').val(), date_of_leaving : $('#date_of_leaving').val(), csrfmiddlewaretoken: csrftoken },
            dataType: 'json',
            success: function( data ) 
        {
            $("#nk-block-top").load(location.href + " #nk-block-top");
        }
        })
});