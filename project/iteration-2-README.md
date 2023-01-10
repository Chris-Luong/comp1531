# COMP1531 Major Project

**✨ Teamwork makes the [UNSW] Dream[s] work 🌈**

## Contents

1. Aims
2. Overview
3. Iteration 1: Basic functionality and tests
4. Iteration 2: Building a web server
5. Iteration 3: Completing the lifecycle
6. Interface specifications
7. Style and documentation
8. Due Dates and Weightings
9. Other Expectations
10. Plagiarism

## 0. Change Log

- 12/03: Extended Iteration due date by 1 day, fixed up marking criteria to add to 100%
- 14/03: See commit for more info, non-trivial clarifications include:
  - Correct `error.py` file pushed to repository
  - Clarity on `handle_str` length when updating str
  - Adding some missing locations that show when behaviour on channels is the same as behaviour on DMs
  - Clarity on behaviour on how contents of messages are changed when an admin removes a user
  - Valid email format re-added to spec (accidentally removed)
  - Clarified the data type of `notifications`
  - `dm/create/v1` behaviour clarified
  - `message/share/v1` behaviour clarified in cases where no message is given
  - <b>Behaviour of `handle` generation on `auth/register` clarified. The handle is truncated to 20 characters during concatenation, but the process of adding the number at the end can extend the 20 characters.</b> For groups that have implemented this behaviour differently (as per some forum posts), you are allowed to keep that implementation and you will not lose marks.
- 16/03:
  - Clarified that messages from users in a channel should remain after they leave the channel
  - Clarified the parameters of dm/create
  - Specified that the creator of a DM is also the owner
- 20/03: Fixed parameters of dm/create
- 26/03: Removed "React" from the notification data type, as that isn't until iteration 3

## 1. Aims:

- To provide students with hands on experience testing, developing, and maintaining a backend server in python.
- To develop students' problem solving skills in relation to the software development lifecycle.
- Learn to work effectively as part of a team by managing your project, planning, and allocation of responsibilities among the members of your team.
- Gain experience in collaborating through the use of a source control and other associated modern team-based tools.
- Apply appropriate design practices and methodologies in the development of their solution
- Develop an appreciation for product design and an intuition of how a typical customer will use a product.

## 2. Overview

To manage the transition from trimesters to hexamesters in 2020, UNSW has established a new focus on building an in-house digital collaboration and communication tool for groups and teams to support the high intensity learning environment.

Rather than re-invent the wheel, UNSW has decided that it finds the functionality of **<a href="https://www.microsoft.com/en-au/microsoft-teams/group-chat-software">Microsoft Teams</a>** to be nearly exactly what it needs. For this reason, UNSW has contracted out Penguin Pty Ltd (a small software business run by Hayden) to build the new product. In UNSW's attempt to try and add a lighter not to the generally fatigued and cynical student body, they have named their UNSW-based product **UNSW Dreams** (or just **Dreams** for short). **UNSW Dreams** is the communication tool that allows you to share, communication, and collaborate to (attempt to) make dreams a reality.

Penguin Pty Ltd has sub-contracted two software firms:

- BlueBottle Pty Ltd (two software developers, Andrea and Andrew, who will build the initial web-based GUI)
- YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in 21T1), who will build the backend python server and possibly assist in the GUI later in the project

In summary, UNSW contracts Penguin Pty Ltd, who sub contracts:

- BlueBottle (Andrea and Andrew) for front end work
- YourTeam (you and others) for backend work

Penguin Pty Ltd met with Andrea and Andrew (the front end development team) 2 weeks ago to brief them on this project. While you are still trying to get up to speed on the requirements of this project, Andrea and Andrew understand the requirements of the project very well.

Because of this they have already specified a **common interface** for the frontend and backend to operate on. This allows both parties to go off and do their own development and testing under the assumption that both parties will comply with the common interface. This is the interface **you are required to use**

Besides the information available in the interface that Andrea and Andrew provided, you have been told (so far) that the features of **Dreams** that UNSW would like to see implemented include:

1. Ability to login, register if not registered, and log out
2. Ability to reset password if forgotten
3. Ability to see a list of channels
4. Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
5. Within a channel, ability to view all messages, view the members of the channel, and the details of the channel
6. Within a channel, ability to send a message now, or to send a message at a specified time in the future
7. Within a channel, ability to edit, share between channels, remove, pin, unpin, react, or unreact to a message
8. Ability to view anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)
9. Ability to search for messages based on a search string
10. Ability to modify a user's admin permissions: (MEMBER, OWNER)
11. Ability to begin a "standup", which is an X minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users
12. Ability to send message directly to a user (or group of users) via direct messaging (DM).

The specific capabilities that need to be built for this project are described in the interface at the bottom. This is clearly a lot of features, but not all of them are to be implemented at once (see below)

## 3. Iteration 1: Basic functionality and tests

This iteration is now complete. Please see commit history to view information pertaining to iteration 1.

## 4. Iteration 2: Building a web server

### 4.1. Task

**NOTE:** In merging the instructions for this iteration into your repo, you may get a failed pipeline. This is most likely because your code is not pylint compliant. If this is the case, that is the _first_ thing you should address for this iteration. It is important you have a _stable_ master branch before proceeding to add additional features.

In this iteration, more features were added to the specification, and the focus has been changed to HTTP endpoints. Many of the theory surrounding iteration 2 will be covered in week 4-6 lectures. Note that there will still be 1 or 2 features of the frontend that will not work because the routes will not appear until iteration 3.

In this iteration, you are expected to:

1. Implement and test the HTTP Flask server according to the entire interface provided in the specification.

   - Part of this section may be automarked.

   - Pylint has been added to your continuous integration file, meaning that code that isn't pylint compliant will now fail the pipeline. The provided `.pylintrc` file is _very_ lenient, so there is no reason you should have to disable any additional checks.

   - Additionally, CI pipelines will measure _branch_ coverage for all `.py` files that aren't tests. The coverage percentage for master is visible in a badge at the top of this repo and changes in coverage will appear in Merge Requests. Do note that coverage of `server.py` is not measured, nor will what is executed by your HTTP tests. This is because, when running HTTP tests, the server is run in a separate process.

   - Your implementation should build upon your work in iteration 1, and ideally your HTTP layer is just a wrapper for underlying functions you've written that handle the logic. Your implementation will rely on topics taught in week 4 (HTTP servers and testing) as well as week 5 (authentication and authorisation).

   - Your implementation will need to implement persistence of data (see section 4.4).

   - You can structure your tests however you choose, as long as they are appended with `_test.py`. It's important you consider how to separate (or combine) your **unit/integration** tests from iteration 1 with the extra **system** tests (HTTP with requests library) in iteration 2. You will be marked on both tests being present/used in this iteration. **An example of a HTTP test has been provided for you in `http_tests/echo_http_test.py`**.

   - You do not have to rewrite all of your pytests as HTTP tests - the latter can test the system at a higher level. For example, to test a success case for `message/send` via HTTP routes you will need to call `auth/register` and `channels/create`; this means you do not need the success case for those two functions seperately. Your HTTP tests will need to cover all success/error conditions for each endpoint, however.

   - Ensure that you correctly manage sessions and tokens in terms of authentication and authorisation, as per requirements laid out in section 6.9

2. Continue demonstrating effective project management and effective git usage

   - Part of this section may be automarked.

   - You will be heavily marked for your use of thoughtful project management and use of git effectively. The degree to which your team works effectively will also be assessed.

   - As for iteration 1 all task tracking and management will need to be done via the GitLab Taskboard.

   - You are required to regularly and thoughtfully make merge requests for the smallest reasonable units, and merge them into `master`.

To run the server you should always use the command

```bash
python3 src/server.py
```

This will start the server on the next available port. If you get any errors relating to `flask_cors`, ensure you have installed all the necessary Python libraries for this course (the list of libraries was updated for this iteration). You can do this with:

```bash
pip3 install $(curl https://www.cse.unsw.edu.au/~cs1531/21T1/requirements.txt)
```

A frontend has been built by Andrea and Andrew that you can use in this iteration, and use your backend to power it (note: an incomplete backend will mean the frontend cannot work). **You can, if you wish, make changes to the frontend code, but it is not required for this iteration.** The source code for the frontend is only provided for your own fun or curiosity.

### 4.2. Implementing and testing features

You should first approach this project by considering its distinct "features". Each feature should add some meaningful functionality to the project, but still be as small as possible. You should aim to size features as the smallest amount of functionality that adds value without making the project more unstable. For each feature you should:

1. Create a new branch.
2. Write tests for that feature and commit them to the branch.
3. Implement that feature.
4. Make any changes to the tests such that they pass with the given implementation. You should not have to do a lot here. If you find that you are, you're not spending enough time on step 2.
5. Create a merge request for the branch.
6. Get someone in your team who **did not** work on the feature to review the merge request. When reviewing, **not only should you ensure the new feature has tests that pass, but you should also check that the coverage percentage has not been significantly reduced.**
7. Fix any issues identified in the review.
8. Merge the merge request into master.

For this project, a feature is typically sized somewhere between a single function, and a whole file of functions (e.g. `auth.py`). It is up to you and your team to decide what each feature is.

There is no requirement that each feature be implemented by only one person. In fact, we encourage you to work together closely on features, especially to help those who may still be coming to grips with python.

Please pay careful attention to the following:

Your tests, keep in mind the following:

- We want to see **evidence that you wrote your tests before writing the implementation**. As noted above, the commits containing your initial tests should appear _before_ your implementation for every feature branch. If we don't see this evidence, we will assume you did not write your tests first and your mark will be reduced.
- You should have black-box tests for all tests required (i.e. testing each function/endpoint). However, you are also welcome to write whitebox unit tests in this iteration if you see that as important.
- Merging in merge requests with failing pipelines is **very bad practice**. Not only does this interfere with your teams ability to work on different features at the same time, and thus slow down development, it is something you will be penalised for in marking.
- Similarly, merging in branches with untested features is also **very bad practice**. We will assume, and you should too, that any code without tests does not work.
- Pushing directly to `master` is not possible for this repo. The only way to get code into master is via a merge request. If you discover you have a bug in `master` that got through testing, create a bugfix branch and merge that in via a merge request.

### 4.3. Recommended approach

Our recommendation with this iteration is that you:

1. Start out trying to implement the new functions the same way you did in iteration 1 (a series of implemented functions, categorised in files, with black-box pytests testing them).
2. Write another layer of HTTP tests that test the inputs/outputs on routes according to the specific, and while writing tests for each component/feature, write the Flask route/endpoint for that feature too.

This approach means that you can essentially finish the project/testing logic without worrying about HTTP, and then simply wrap the HTTP/Flask layer on top of it at the end.

### 4.4. Storing data

You are required to store data persistently in this iteration.

Modify your backend such that it is able to persist and reload its data store if the process is stopped and started again. The persistence should happen at regular intervals so that in the event of unexpected program termination (e.g. sudden power outage) a minimal amount of data is lost. You may implement this using whatever method of serialisation you prefer (e.g. pickle, JSON).

### 4.5. Submission

This iteration due date and demonstrate week is described in section 7. You will demonstrate this submission inline with the information provided in section 7.

### 4.6. Versioning

You might notice that some routes are suffixed with `v1` and `v2`, and that all the new routes are `v1` yet all the old routes are `v2`. Why is this? When you make changes to specifications, it's usually good practice to give the new function/capability/route a different unique name. This way, if people are using older versions of the specification they can't accidentally call the updated function/route with the wrong data input.

Hint: Yes, your `v2` routes can use the `X_Y_v1` functions you had in iteration 1, regardless of whether you rename the functions or not. The layer of abstraction in iteration 2 has changed from the function interface to the HTTP interface, and therefore your 'functions' from iteration 1 are essentailly now just implementation details, and therefore are completely modifiable by you.

### 4.7. Marking Criteria

<table>
  <tr>
    <th>Section</th>
    <th>Weighting</th>
    <th>Criteria</th>
  </tr>
  <tr>
    <td>Automarking (Testing)</td>
    <td>15%</td>
    <td><ul>
      <li>Correctly written tests based on the specification requirements</li>
      <li>Code coverage (99% coverage gives 30% of the marks for this section)</li>
    </ul>
  </td>
  </ul>
  <tr>
    <td>Automarking (Implementation)</td>
    <td>35%</td>
    <td><ul>
      <li>Correct implementation of specified functions</li>
      <li>Correctly linted code (worth 10% of this section)</li>
    </ul>
  </td>
  </ul>
  <tr>
    <td>Code Quality</td>
    <td>30%</td>
    <td><ul>
      <li>Demonstrated an understanding of good test <b>coverage</b></li>
      <li>Demonstrated an understanding of the importance of <b>clarity</b> on the communication test and code purposes</li>
      <li>Demonstrated an understanding of thoughtful test <b>design</b></li>
      <li>Appropriate use of python data structures (lists, dictionaries, etc.)</li>
      <li>Appropriate style as described in section 8.4</li>
      <li>Appropriate application of good software design and pythonic patterns</li>
      <li>Implementation of persistent state</li>
    </ul>
  </td>
  </ul>
  <tr>
    <td>Git & Project Management</td>
    <td>20%</td>
    <td><ul>
      <li>Meaningful and informative git commit names being used</li>
      <li>At least 12 merge requests into master made</li>
      <li>A generally equal contribution between team members</li>
      <li>Clear evidence of reflection on group's performance and state of the team, with initiative to improve in future iterations</li>
      <li>Effective use of course-provided MS Teams for communicating, demonstrating an ability to communicate and manage effectivelly digitally</li>
      <li>Use of task board on Gitlab to track and manage tasks</li>
      <li>Effective use of agile methods such as standups</li>
      <li>Minutes/notes taken from group meetings (and stored in a logical place in the repo)</li>
    </ul>
  </td>
  </tr>
</table>

For this and for all future milestones, you should consider the other expectations as outlined in section 8 below.

## 5. Iteration 3: Completing the lifecycle

Coming Soon

## 6. Interface specifications

These interface specifications come from Andrea and Andrew, who are building the frontend to the requirements set out below.

### 6.1. Data types

<table>
  <tr>
    <th>Variable name</th>
    <th>Type</th>
  </tr>
  <tr>
    <td>named exactly <b>email</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>has suffix <b>id</b></td>
    <td>integer</td>
  </tr>
  <tr>
    <td>named exactly <b>length</b></td>
    <td>integer</td>
  </tr>
  <tr>
    <td>contains substring <b>password</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>named exactly <b>token</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>named exactly <b>message</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>contains substring <b>name</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>has prefix <b>is_</b></td>
    <td>boolean</td>
  </tr>
  <tr>
    <td>has prefix <b>time_</b></td>
    <td>integer (unix timestamp), [check this out](https://www.tutorialspoint.com/How-to-convert-Python-date-to-Unix-timestamp)</td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>messages</b></td>
    <td>List of dictionaries, where each dictionary contains types { message_id, u_id, message, time_created }</td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>channels</b></td>
    <td>List of dictionaries, where each dictionary contains types { channel_id, name }</td>
  </tr>
  <tr>
    <td>has suffix <b>_str</b></td>
    <td>string</td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>dms</b></td>
    <td>List of dictionaries, where each dictionary contains types { dm_id, name }</td>
  </tr>
  <tr>
    <td>(outputs only) name ends in <b>members</b></td>
    <td>List of dictionaries, where each dictionary contains types of <b>user</b></td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>user</b></td>
    <td>Dictionary containing u_id, email, name_first, name_last, handle_str</td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>users</b></td>
    <td>List of dictionaries, where each dictionary contains types of <b>user</b></td>
  </tr>
  <tr>
    <td>(outputs only) named exactly <b>notifications</b></td>
    <td>List of dictionaries, where each dictionary contains types { channel_id, dm_id, notification_message } where channel_id is the id of the channel that the event happened in, and is <code>-1</code> if it is being sent to a DM. dm_id is the DM that the event happened in, and is <code>-1</code> if it is being sent to a channel. The list should be ordered from most to least recent. Notification_message is a string of the following format for each trigger action:<ul><li>tagged: "{User’s handle} tagged you in {channel/DM name}: {first 20 characters of the message}"</li><li>added to a channel/DM: "{User’s handle} added you to {channel/DM name}"</li></ul>
    </td>
  </tr>
  <tr>
    <td>named exactly <b>u_ids</b></td>
    <td>List of user ids</td>
  </tr>
</table>

### 6.2. Interface

<table>
  <tr>
    <th>Name & Description</th>
    <th>HTTP Method</th>
    <th>Data Types</th>
    <th>Exceptions</th>
  </tr>
  <tr>
    <td><code>auth/login/v2</code><br /><br />Given a registered users' email and password and returns a new `token` for that session</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(email, password)</code><br /><br /><b>Return Type:</b><br /><code>{ token, auth_user_id }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Email entered is not a valid email</li>
        <li>Email entered does not belong to a user</li>
        <li>Password is not correct</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>auth/register/v2</code><br /><br />Given a user's first and last name, email address, and password, create a new account for them and return a new `token` for that session. A handle is generated that is the concatenation of a lowercase-only first name and last name. If the concatenation is longer than 20 characters, it is cutoff at 20 characters. The handle will not include any whitespace or the '@' character. Once you've concatenated it, if the handle is once again taken, append the concatenated names with the smallest number (starting from 0) that forms a new handle that isn't already taken. The addition of this final number may result in the handle exceeding the 20 character limit.</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(email, password, name_first, name_last)</code><br /><br /><b>Return Type:</b><br /><code>{ token, auth_user_id }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li>
        <li>Email address is already being used by another user</li>
        <li>Password entered is less than 6 characters long</li>
        <li>name_first is not between 1 and 50 characters inclusively in length</li>
        <li>name_last is not between 1 and 50 characters inclusively in length</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>auth/logout/v1</code><br /><br />Given an active token, invalidates the token to log the user out. If a valid token is given, and the user is successfully logged out, it returns true, otherwise false.</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ is_success }</code></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>channel/invite/v2</code><br /><br />Invites a user (with user id u_id) to join a channel with ID channel_id. Once invited the user is added to the channel immediately</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id, u_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>channel_id does not refer to a valid channel.</li>
        <li>u_id does not refer to a valid user</li>
      </ul>
      <b>AccessError</b> when any of:
      <ul>
        <li>the authorised user is not already a member of the channel</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channel/details/v2</code><br /><br />Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id)</code><br /><br /><b>Return Type:</b><br /><code>{ name, is_public, owner_members, all_members }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
      </ul>
      <b>AccessError</b> when any of:
      <ul>
        <li>Authorised user is not a member of channel with channel_id</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channel/messages/v2</code><br /><br />Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id, start)</code><br /><br /><b>Return Type:</b><br /><code>{ messages, start, end }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
        <li>start is greater than the total number of messages in the channel</li>
      </ul>
      <b>AccessError</b> when any of:
      <ul>
        <li>Authorised user is not a member of channel with channel_id</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channel/join/v2</code><br /><br />Given a channel_id of a channel that the authorised user can join, adds them to that channel</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
      </ul>
      <b>AccessError</b> when any of:
      <ul>
        <li>channel_id refers to a channel that is private (when the authorised user is not a global owner)</li>
      </ul>
    </td>
  </tr>

  <tr>
    <td><code>channel/addowner/v1</code><br /><br />Make user with user id u_id an owner of this channel</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id, u_id)</code><br /><br /><b>Return Type:</b><code>{}</code>
    </td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
        <li>When user with user id u_id is already an owner of the channel</li>
      </ul>
      <b>AccessError</b> when the authorised user is not an owner of the **Dreams**, or an owner of this channel</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channel/removeowner/v1</code><br /><br />Remove user with user id u_id an owner of this channel</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id, u_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
        <li>When user with user id u_id is not an owner of the channel</li>
        <li>The user is currently the only owner</li>
      </ul>
      <b>AccessError</b> when the authorised user is not an owner of the **Dreams**, or an owner of this channel</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channel/leave/v1</code><br /><br />Given a channel ID, the user removed as a member of this channel. Their messages should remain in the channel</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Channel ID is not a valid channel</li>
      </ul>
      <b>AccessError</b> when
      <ul>
        <li>Authorised user is not a member of channel with channel_id</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>channels/list/v2</code><br /><br />Provide a list of all channels (and their associated details) that the authorised user is part of</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ channels }</code></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>channels/listall/v2</code><br /><br />Provide a list of all channels (and their associated details)</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ channels }</code></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>channels/create/v2</code><br /><br />Creates a new channel with that name that is either a public or private channel</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, name, is_public)</code><br /><br /><b>Return Type:</b><br /><code>{ channel_id }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Name is more than 20 characters long</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>message/send/v2</code><br /><br />Send a message from authorised_user to the channel specified by channel_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel.</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, channel_id, message)</code><br /><br /><b>Return Type:</b><br /><code>{ message_id }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Message is more than 1000 characters</li>
      </ul>
        <b>AccessError</b> when: <li> the authorised user has not joined the channel they are trying to post to</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>message/edit/v2</code><br /><br />Given a message, update its text with new text. If the new message is an empty string, the message is deleted.</td>
    <td style="font-weight: bold; color: brown;">PUT</td>
    <td><b>Parameters:</b><br /><code>(token, message_id, message)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Length of message is over 1000 characters</li>
        <li>message_id refers to a deleted message</li>
      </ul>
      <b>AccessError</b> when none of the following are true:
      <ul>
        <li>Message with message_id was sent by the authorised user making this request</li>
        <li>The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>message/remove/v1</code><br /><br />Given a message_id for a message, this message is removed from the channel/DM</td>
    <td style="color: red; font-weight: bold;">DELETE</td>
    <td><b>Parameters:</b><br /><code>(token, message_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Message (based on ID) no longer exists</li>
      </ul>
      <b>AccessError</b> when none of the following are true:
      <ul>
        <li>Message with message_id was sent by the authorised user making this request</li>
        <li>The authorised user is an owner of this channel (if it was sent to a channel) or the **Dreams**</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>message/share/v1</code><br /><br /><code>og_message_id</code> is the original message. <code>channel_id</code> is the channel that the message is being shared to, and is <code>-1</code> if it is being sent to a DM. <code>dm_id</code> is the DM that the message is being shared to, and is <code>-1</code> if it is being sent to a channel.
    <code>message</code> is the optional message in addition to the shared message, and will be an empty string <code>''</code> if no message is given</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, og_message_id, message, channel_id, dm_id)</code><br /><br /><b>Return Type:</b><br /><code>{shared_message_id}</code></td>
    <td>AccessError when: <ul><li>the authorised user has not joined the channel or DM they are trying to share the message to</li>
    </ul> </td>
  </tr>
  <tr>
    <td><code>dm/details/v1</code><br /><br />Users that are part of this direct message can view basic information about the DM</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id)</code><br /><br /><b>Return Type:</b><br /><code>{ name, members }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>DM ID is not a valid DM</li>
      </ul>
      <b>AccessError</b> when
      <ul>
        <li>Authorised user is not a member of this DM with dm_id</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>dm/list/v1</code><br /><br />Returns the list of DMs that the user is a member of</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ dms }</code></td>
    <td> N/A </td>
  </tr>
  <tr>
    <td><code>dm/create/v1</code><br /><br /><code>u_ids</code> contains the user(s) that this DM is directed to, and will not include the creator. The creator is the owner of the DM. <code>name</code> should be automatically generated based on the user(s) that is in this dm. The name should be an alphabetically-sorted, comma-separated list of user handles, e.g. 'handle1, handle2, handle3'.</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, u_ids)</code><br /><br /><b>Return Type:</b><br /><code>{ dm_id, dm_name }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li> u_id does not refer to a valid user</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>dm/remove/v1</code><br /><br />Remove an existing DM. This can only be done by the original creator of the DM.</td>
    <td style="color: red; font-weight: bold;">DELETE</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td> InputError when: <ul> <li> dm_id does not refer to a valid DM </li>
    </ul>
    <b>AccessError</b> when: <ul> <li>the user is not the original DM creator</li>
    </ul>

  </td>
  </tr>
  <tr>
    <td><code>dm/invite/v1</code><br /><br />Inviting a user to an existing dm</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id, u_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td> <b>InputError</b> when any of: <ul>
         <li> dm_id does not refer to an existing dm.</li>
         <li> u_id does not refer to a valid user. </li>
       </ul>
        <b>AccessError</b> when: <ul>
        <li>the authorised user is not already a member of the DM</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>dm/leave/v1</code><br /><br />Given a DM ID, the user is removed as a member of this DM</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>dm_id is not a valid DM</li>
      </ul>
      <b>AccessError</b> when
      <ul>
        <li>Authorised user is not a member of DM with dm_id</li>
      </ul>
    </td>
  </tr>
  <tr>
     <td><code>dm/messages/v1</code><br /><br />Given a DM with ID dm_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id, start)</code><br /><br /><b>Return Type:</b><br /><code>{ messages, start, end }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>DM ID is not a valid DM</li>
        <li>start is greater than the total number of messages in the channel</li>
      </ul>
      <b>AccessError</b> when any of:
      <ul>
        <li>Authorised user is not a member of DM with dm_id</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>message/senddm/v1</code><br /><br />Send a message from authorised_user to the DM specified by dm_id. Note: Each message should have it's own unique ID. I.E. No messages should share an ID with another message, even if that other message is in a different channel or DM.</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, dm_id, message)</code><br /><br /><b>Return Type:</b><br /><code>{ message_id }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Message is more than 1000 characters</li>
      </ul>
        <b>AccessError</b> when: <li> the authorised user is not a member of the DM they are trying to post to</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>user/profile/v2</code><br /><br />For a valid user, returns information about their user_id, email, first name, last name, and handle</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, u_id)</code><br /><br /><b>Return Type:</b><br /><code>{ user }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>User with u_id is not a valid user</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>user/profile/setname/v2</code><br /><br />Update the authorised user's first and last name</td>
    <td style="font-weight: bold; color: brown;">PUT</td>
    <td><b>Parameters:</b><br /><code>(token, name_first, name_last)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>name_first is not between 1 and 50 characters inclusively in length</li>
        <li>name_last is not between 1 and 50 characters inclusively in length</ul></ul></li>
  </tr>
  <tr>
    <td><code>user/profile/setemail/v2</code><br /><br />Update the authorised user's email address</td>
    <td style="font-weight: bold; color: brown;">PUT</td>
    <td><b>Parameters:</b><br /><code>(token, email)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>Email entered is not a valid email using the method provided [here](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) (unless you feel you have a better method).</li>
        <li>Email address is already being used by another user</li>
      </ul>
  </tr>  
  <tr>
    <td><code>user/profile/sethandle/v1</code><br /><br />Update the authorised user's handle (i.e. display name)</td>
    <td style="font-weight: bold; color: brown;">PUT</td>
    <td><b>Parameters:</b><br /><code>(token, handle_str)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>handle_str is not between 3 and 20 characters inclusive</li>
        <li>handle is already used by another user</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>users/all/v1</code><br /><br />Returns a list of all users and their associated details</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ users }</code></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>search/v2</code><br /><br />Given a query string, return a collection of messages in all of the channels/DMs that the user has joined that match the query</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token, query_str)</code><br /><br /><b>Return Type:</b><br /><code>{ messages }</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>query_str is above 1000 characters</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>admin/user/remove/v1</code><br /><br />Given a User by their user ID, remove the user from the Dreams. Dreams owners can remove other **Dreams** owners (including the original first owner). Once users are removed from **Dreams**, the contents of the messages they sent will be replaced by 'Removed user'. Their profile must still be retrievable with user/profile/v2, with their name replaced by 'Removed user'. </td>
    <td style="color: red; font-weight: bold;">DELETE</td>
    <td><b>Parameters:</b><br /><code>(token, u_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when
      <ul>
        <li>u_id does not refer to a valid user</li>
        <li>The user is currently the only owner</li>
      </ul>
      <b>AccessError</b> when
      <ul>
        <li>The authorised user is not an owner</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td><code>admin/userpermission/change/v1</code><br /><br />Given a User by their user ID, set their permissions to new permissions described by permission_id</td>
    <td style="font-weight: bold; color: blue;">POST</td>
    <td><b>Parameters:</b><br /><code>(token, u_id, permission_id)</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>
      <b>InputError</b> when any of:
      <ul>
        <li>u_id does not refer to a valid user<li>permission_id does not refer to a value permission</li>
      </ul>
      <b>AccessError</b> when
      <ul>
        <li>The authorised user is not an owner</li>
      </ul></li>
  </tr>
  <tr>
    <td><code>notifications/get/v1</code><br /><br />Return the user's most recent 20 notifications</td>
    <td style="font-weight: bold; color: green;">GET</td>
    <td><b>Parameters:</b><br /><code>(token)</code><br /><br /><b>Return Type:</b><br /><code>{ notifications }</code></td>
    <td>N/A</td>
  </tr>
  <tr>
    <td><code>clear/v1</code><br /><br />Resets the internal data of the application to it's initial state</td>
    <td style="color: red; font-weight: bold;">DELETE</td>
    <td><b>Parameters:</b><br /><code>()</code><br /><br /><b>Return Type:</b><br /><code>{}</code></td>
    <td>N/A</td>
  </tr> 
</table>

### 6.3. Errors for all functions

Either an `InputError` or `AccessError` is thrown when something goes wrong. All of these cases are listed in the **Interface** table.

One exception is that, even though it's not listed in the table, for all functions except `auth/register`, `auth/login`, `auth/passwordreset/request` (iteration 3) and `auth/passwordreset/reset` (iteration 3), an `AccessError` is thrown when the token passed in is not a valid id.

### 6.4. Pagination

The behaviour in which channel_messages returns data is called **pagination**. It's a commonly used method when it comes to getting theoretially unbounded amounts of data from a server to display on a page in chunks. Most of the timelines you know and love - Facebook, Instagram, LinkedIn - do this.

For example, in iteration 1, if we imagine a user with `token` "12345" is trying to read messages from channel with ID 6, and this channel has 124 messages in it, 3 calls from the client to the server would be made. These calls, and their corresponding return values would be:

- channel_messages("12345", 6, 0) => { [messages], 0, 50 }
- channel_messages("12345", 6, 50) => { [messages], 50, 100 }
- channel_messages("12345", 6, 100) => { [messages], 100, -1 }

Pagination should also apply to DMs.

### 6.5. Permissions:

- Members in a channel have one of two channel permissions.
  1.  Owner of the channel (the person who created it, and whoever else that creator adds)
  2.  Members of the channel
- Dreams users have two global permissions
  1.  Owners (permission id 1), who can also modify other owners' permissions.
  2.  Members (permission id 2), who do not have any special permissions
- All **Dreams** users are members by default, except for the very first user who signs up, who is an owner

A user's primary permissions are their global permissions. Then the channel permissions are layered on top. For example:

- An owner of **Dreams** has owner permissions in every channel they've joined
- A member of **Dreams** is a member in channels they are not owners of
- A member of **Dreams** is an owner in channels they are owners of

### 6.6. Token

Many of these functions (nearly all of them) need to be called from the perspective of a user who is logged in already. When calling these "authorised" functions, we need to know:

1. Which user is calling it
2. That the person who claims they are that user, is actually that user

We could solve this trivially by storing the user ID of the logged in user on the front end, and every time the front end (from Andrea and Andrew) calls your background, they just sent a user ID. This solves our first problem (1), but doesn't solve our second problem! Because someone could just "hack" the front end and change their user id and then log themselves in as someone else.

To solve this when a user logs in or registers the backend should return a "token" (an authorisation hash) that the front end will store and pass into most of your functions in future. When these "authorised" functions are called, those tokens returned from register/login will be passed into those functions, and from there you can check if a token or token is valid, and determine the user ID.

Passwords must be stored in an encrypted form, and tokens must use JWTs (or similar).

### 6.7. Working with the frontend

There is a SINGLE repository available for all students at https://gitlab.cse.unsw.edu.au/COMP1531/21T1/project-frontend. You can clone this frontend locally. The course notice said you will receive your own copy of this, however, that isn't necessary anymore since most groups will not modify the frontend repo. If you'd like to modify the frontend repo (i.e. teach yourself some frontend), please FORK the repository.

If you run the frontend at the same time as your flask server is running on the backend, then you can power the frontend via your backend.

#### 6.7.1.

A working example of the frontend can be used at http://**Dreams**-unsw.herokuapp.com/

The data is reset daily, but you can use this link to play around and get a feel for how the application should behave.

#### 6.7.2. Error raising for the frontend

For errors to be appropriately raised on the frontend, they must be raised by the following:

```python
if True: # condition here
    raise InputError(description='Description of problem')
```

The descriptions will not be assessed, they are just there for the frontend to help users.

The types in error.py have been modified appropriately for you.

### 6.8. Tagging users

A user is tagged when a message contains the @ symbol, followed immediately by the user’s handle. If the handle is invalid, or the user is not a member of the channel or DM, no one is tagged.

### 6.9. User Sessions

Iteration 2 introduces the concept of `sessions`. With sessions, when a user logs in or registers, they receive a "token" (think of it like a ticket to a concert). These tokens are stored on the web browser, and nearly every time that user wants to make a request to the server, they will pass this "token" as part of this request. In this way, the server is able to take this token, look at it (like checking a ticket), and determine whether it's really you or not.

This notion of a session is explored in the authentication (Hashing) & authorisation (JWT), and is an expectation that it is implemented in iteration 2 and beyond.

For iteration 2 and beyond, we also expect you to handle multiple concurrent sessions. I.E. One user can log in on two different browser tabs, click logout on tab 1, but still functionally use the website on tab 2.

### 6.10. Valid email format

A valid email should match the following regular expression:

```
'^[a-zA-Z0-9]+[\\._]?[a-zA-Z0-9]+[@]\\w+[.]\\w{2,3}$'
```

The python `re` (regular expression) module allows you to determine whether a string matches a regular expression. You do not need to understand regular expressions to effectively utilise the `re` module to check if the email is correct.

## 7. Due Dates and Weightings

| Iteration | Due date                             | Demonstration to tutor(s)      | Assessment weighting of project (%) |
| --------- | ------------------------------------ | ------------------------------ | ----------------------------------- |
| 1         | 10am Monday 8th March (**week 4**)   | In YOUR **week 4** laboratory  | 30%                                 |
| 2         | 10am Tuesday 6th April (**week 8**)  | In YOUR **week 8** laboratory  | 40%                                 |
| 3         | 10am Monday 19th April (**week 10**) | In YOUR **week 10** laboratory | 30%                                 |

### 7.1. Late Penalties

There is no late penalty, as we do not accept late submissions. You will be assessed on the most recent version of your work at the due date and time listed. We will automatically collect and submit the code that is on the `master` branch of your repository.

If the deadline is approaching and you have features that are either untested or failing their tests, **DO NOT MERGE IN THOSE MERGE REQUESTS**. Your tutor will look at unmerged branches and may allocate some reduced marks for incomplete functionality, but `master` should only contain working code.

### 7.2. Demonstration

For the demonstrations in weeks 4, 8, and 10, all team members **must** attend this lab session, or they will not receive a mark.

When you demonstrate this iteration in your lab time, it will consist of a 15 minute Q&A either in front of your tutor and some other students in your tutorial. For online classes, webcams are required to be on during this Q&A (your phone is a good alternative if your laptop/desktop doesn't have a webcam).

## 8. Other Expectations

While it is up to you as a team to decide how work is distributed between you, for the purpose of assessment there are certain key criteria all members must.

- Code contribution
- Documentation contribution
- Usage of git/GitLab
- Attendance
- Peer assessment
- Academic conduct

The details of each of these is below.

While, in general, all team members will receive the same mark (a sum of the marks for each iteration), **if you as an individual fail to meet these criteria your final project mark may be scaled down**, most likely quite significantly.

### 8.1. Project check-in

During your lab class, in weeks without project demonstrations, you and your team will conduct a short stand-up in the presence of your tutor. Each member of the team will briefly state what they have done in the past week, what they intend to do over the next week, and what issues they faced or are currently facing. This is so your tutor, who is acting as a representative of the client, is kept informed of your progress. They will make note of your presence and may ask you to elaborate on the work you've done.

Project check-ins are also excellent opportunities for your tutor to provide you with both technical and non-technical guidance.

### 8.2. Code contribution

All team members must contribute code to the project to a generally similar degree. Tutors will assess the degree to which you have contributed by looking at your **git history** and analysing lines of code, number of commits, timing of commits, etc. If you contribute significantly less code than your team members, your work will be closely examined to determine what scaling needs to be applied.

### 8.3. Documentation contribution

All team members must contribute documentation to the project to a generally similar degree. Tutors will assess the degree to which you have contributed by looking at your **git history** but also **asking questions** (essentially interviewing you) during your demonstration.

Note that, **contributing more documentation is not a substitute for not contributing code**.

### 8.4. Code Style and Documentation

You are required to ensure that your code:

- Follows pythonic principles discussed in lectures and tutorials
- Follows stylistic convenctions discussed in lectures and tutorials
- (For iterations 2 & 3) your code should achieve a `10.00/10` `pylint` score

Examples of things to focus on include:

- Correct casing of variable, function and class names
- Meaningful variable and function names
- Readability of code and use of whitespace
- Modularisation and use of helper functions where needed

Your functions such as `auth_register`, `channel_invite`, `message_send`, etc. are also required to contain docstrings of the following format:

```
<Brief description of what the function does>

Arguments:
    <name> (<data type>)    - <description>
    <name> (<data type>)    - <description>
    ...

Exceptions:
    InputError  - Occurs when ...
    AccessError - Occurs when ...

Return Value:
    Returns <return value> on <condition>
    Returns <return value> on <condition>
```

In each iteration you will be assessed on ensuring that every relevant function/endpoint in the specification is appropriately documented.

### 8.5. Peer Assessment

There will be a mid-term peer assessment around Week 5 where you will rate each team member's contribution to the project up until that point and have the chance to raise concerns with any team members in writing.

You will be required to complete a form in week 10 where you rate each team member's contribution to the project and leave any comments you have about them. Information on how you can access this form will be released closer to Week 10.

Your other team members will **not** be able to see how you rated them or what comments you left in either peer assessment. If your team members give you a less than satisfactory rating, your contribution will be scrutinised and you may find your final mark scaled down.

### 8.6. Attendance

It is generally assumed that all team members will be present at the demonstrations and at weekly check-ins. If you're absent for more than 80% of the weekly check-ins or any of the demonstrations, your mark may be scaled down.

If, due to exceptional circumstances, you are unable to attend your lab for a demonstration, inform your tutor as soon as you can so they can record your absence as planned.

## 10. Plagiarism

The work you and your group submit must be your own work. Submission of work partially or completely derived from any other person or jointly written with any other person is not permitted. The penalties for such an offence may include negative marks, automatic failure of the course and possibly other academic discipline. Assignment submissions will be examined both automatically and manually for such submissions.

Relevant scholarship authorities will be informed if students holding scholarships are involved in an incident of plagiarism or other misconduct.

Do not provide or show your project work to any other person, except for your group and the teaching staff of COMP1531. If you knowingly provide or show your assignment work to another person for any reason, and work derived from it is submitted you may be penalized, even if the work was submitted without your knowledge or consent. This may apply even if your work is submitted by a third party unknown to you.

Note, you will not be penalized if your work has the potential to be taken without your consent or knowledge.
