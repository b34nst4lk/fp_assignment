# 4

Preface: While the answers below are somewhat idealistic, I say them with the
understanding that teams do not necessarily have the time, bandwidth, resources
or experience to do refactoring or testing. While it is best practice to do these
activities, I understand that every team has their own constraints, and any
exercise to encourage both activities does need to account for the circumstances
of the team.

## 4a. Refactoring
### What is refactoring?

Refactoring is the act of studying existing working code, and doing the necessary 
restructuring of code while keeping the functionality intact. The goal of refactoring 
is to ensure the long term maintainability of code.

### When should you refactor?

In my opinion, the best practice for refactoring is to do it as soon as possible. 
In the practice of test-driven development (TDD), we should write a test case, 
write code to pass the test, and refactor to tidy up the code.

However, it is easier said than done. It is common for teams and organizations
to neglect testing, and the subsequent refactoring in the rush to deliver
features that actually benefit the company.

Having said that, you should refactor only *when you can guarantee that everything*
*works as required* after the change is made. Hence, having a reliable suite of tests,
whether manual or automated, is an essential prerequisite to refactoring.

### Why should you refactor?

Code is read more often than it is written. Engineers will, relatively speaking, rarely have
the opportunity to write completely new code from scratch in a workplace environment.
As such, refactoring with the goal of long term maintainability is the act of being
considerate to others and our future selves so that code remains legible even after
it hasn't been touched for a long time.

Refactoring is also an exercise of finding common patterns and abstractions. Was
there a particular feature that was built by copying, pasting and then making modifications?
That is likely to be a good candidate for abstraction if the logic is truly shared.


## 4b. Testing
### What is testing?

Testing is the act of ensuring that code promising to meet requirements actually do
meet said requirements. Testing broadly falls into two categories, manual and
automated testing. Manual testing is having a person clicking through buttons, or
clicking on Postman to fire a request, or running a process and checking the database
for the result by hand. Automated testing formalizes as much of that as possible
in code.

There are also different levels of testing. At the very bottom, we test if an 
interface that a user (in this case a developer), such as a function, can interact
with. 

### When should you test?

The best time to test is before code is written. The next best time was yesterday,
and a close third is now. In addition, when we discover a bug caused by mistakes
in code, we should write a test for that, as a bug is a requirement not met.

Having said that, as with refactoring, the pressure to deliver can create a culture
where testing is deprioritized and become neglected as a result. The urgency to
add tests is still present, but the longer tests are not present, the more care 
is needed to plan for testing, as the code is likely structured in a way that is
difficult to test.

### Why should you test?

Every requirement that is agreed upon is a contract between the engineer and the
user. The user can be a customer, a stakeholder, or another engineer, depending
on what is being built. Testing helps us to confidently guarantee that we have
delivered as promised.
