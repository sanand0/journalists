# Prompts

<!--

cd /home/sanand/code/journalists/flaps/print-to-online
dev.sh
claude --dangerously-skip-permissions
-->

## Convert Print to HTML

See, we have this problem. This originals/ directory contains a bunch of flaps. Flaps are things that we publish on the Times of India. These are meant for print. Take a look at the PDF files and the corresponding SVG files. Now, you can guess why this would be hard to publish online. Now, I want you to go research the Times of India website. See what is the format that they are using, how things are laid out, etc. Research these flaps as well. Look at the content, look at the graphics, etc. And figure out a plan by which you can convert the SVG files or flaps like these into HTML that can be published on Times of India. Remember that the objective is not to reproduce the flaps exactly as they are. They are often too tall, for example. The point is to repurpose this in a way that is online friendly and highly engaging. With that objective in mind, create an approach and convert maybe three flaps, possibly in slightly different ways, so that I can take a look at the output and give feedback. Then you can use that feedback to create an approach that you can run every time. In case you are stuck anywhere or have any problems or want some clarifications, you can pause and ask me, or at the end of it, give me a list of questions that I should answer that will help you decide what is the best approach.

Save the output HTML files in the output/ directory. Create a notes-v1.md that explains your approach, how to run the code, what questions you have, etc.

---

The objective is to create HTML that, when pasted into the Times of India CMS, it will be indistinguishable from the HTML that they create for their own articles.
Use rodney / playwright to take screenshots of the generated HTMLs as well as the Times of India website.
Inspect visually. Also inspect the TOI website HTML.
Fix all design and code consistency issues - align even small things like actual choice of font, colors, spacing, etc.
Make sure that it's responsive.

Document updates and corrections in notes-v1.md in a new section.
