# COMP1531 Project Assumptions (Tue13c Dorritos)  
  
  
<h1> General </h1>  
  
- Data is stored correctly according to the  
specification and criteria e.g. data can be  
obtained from a structure called 'data' in  
an empty file presumabbly called 'data.py'.  
  
<h1> channel.py </h1>  
  
  
<h2> channel_invite_v1 </h2>  
  
- All channel members can invite other users into the channel  
- when invited the users u_id is stored in the channel members 
  
<h2> channel_details_v1 </h2>  
  
- All members in channel can view details  
- When creating a channel, all the members' data  
is updated into the database (as per our implementation)  
  
<h2> channel_messages_v1 </h2>  
  
- channel_id starts at 1  
- When sending messages, they are sorted into channels  


<h1> dm_test.py </h1>  

- First user has u_id of 0  
- First dm has dm_id of 0  
- dm_create_v1 works  

<h2> test_dm_remove_v1 </h2>  

- Assumes dm_list_v1 works  

<h2> test_dm_details_v1 </h2>  

- Assumes dm_invite_v1 works  

<h1> dm.py </h1>  


<h2> dm_details </h2>  

- Both members and owners can view basic information about the dm  

<h2> dm_create </h2>  

- Name generated should include the handle of the owner    

<h2> dm_invite </h2>  

- Both members and owners can invite other users into the channel   

<h2> dm_leave </h2>  

- If the Dm owner leaves the dm, the dm still exists however the owner changes  


<h1> message.py </h1>  


<h2> message_send </h2>  

- only one message can be sent at a time  
- a message can be sent to multiple users at once


<h1> auth.py </h1>  


<h2> auth_login </h2>  

- If you are already logged in, login shouldnt fail  
- Token is constructed from the u_id


<h2> auth_register </h2>  

- Users can have the same first name and last name but will have different u_ids  
- Token acts as a registration key  
