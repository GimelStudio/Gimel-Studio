# How to contribute to Gimel Studio

Thank you for wanting to contribute to this open-source project! All contributions will be given due credit. :)

If you have any questions about contributing, feel free to ask.

Make sure to take a look at the [ROADMAP.txt](ROADMAP.txt) too. :)


## Tips

A few tips when developing Gimel Studio:

- Make sure the ```APP_DEBUG``` setting in *src>GimelStudio>meta.py* is set to ```True```. This disables features such as the splashscreen, etc. which would otherwise hinder development and enables features like being able to show the node you are developing by default.
- If you're looking to develop new nodes, have a look at the *src>corenodes* directory where all the core nodes in Gimel Studio live. Much of the time, you can copy-and-paste the same properties and/or find a solution to a problem you've come across.


# Code Standards

The code largly follows Pep8, with the exceptions that the line length is allowed to be longer than the Pep8 character limit and ``TitleCase`` is used to preserve consistency with wxPython methods.


## Bugs (*You found a bug*)

* **Ensure the bug was not already reported** by searching on the GitHub issues.

* If you're unable to find an open issue addressing the problem, [open a new issue](https://github.com/Correct-Syntax/Gimel-Studio/issues/new). Be sure to include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.


## Bug fixes (*You wrote a patch that fixes a bug*)

* Open a new GitHub pull request with the patch.

* Ensure the pull request description clearly describes the problem and solution. Include the relevant issue number if applicable.


## Ideas, New Features, Feature Changes (*You intend to add a new feature or change an existing one*)

Feel free to join the Gimel Studio [Discord Server](https://discord.gg/RqwbDrVDpK) or [Gitter Community](https://gitter.im/Gimel-Studio/community) if you are interested in discussing design/development of Gimel Studio or have any questions.

Feel free to offer feature suggestions, ideas, or let me know if you want to make a change to something. **This ensures that you don't end up re-working on the same thing as me, @Correct-Syntax!** I always welcome constructive feedback from others.