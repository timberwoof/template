Templating system so that multiple versions of some program file can exist based off a single template. 

Statement of Problem
--------------------
For example, there are four Black Gazza doors with very similar functionality. 
Differences lie in things like geometry and numbers of prims and faces. 
Often the same basic bug exists in all four versions, 
and I'd like to be able to fix it in one place and have the fix propagate to the other versions. 
Git is not the right way to do this; it doesn't know what code change needs to go into all versions 
and what code change needs to be in just this version. 

In the simplest case there would be three sets of files: 
One Template file which contains the main code and start/stop markers for substitutions. 

A number of Content files which contain the substitutions. 
A Content file would have a marker that tells which Template file it goes with. 

An equal number of Merged files which contain the Template with the Content substituted in. 
A Merged file would have a marker that tells which Template file and which Content file created it. 
The Merged files would be deployed into the doors. 

I want to be able to edit any of the (Template, Content, or Merged) files 
and propagate the changes appropriately. 

The Merge program would take a Content file name as a parameter. 
It would read the Content file and the Template file, and spit out the Merged file. 

The Unmerge program would take a Merged file name as a parameter. 
It would read the Merged file and spit out the template file and the Content file. 

The purpose of this two-way merge-unmerge is that one can debug actual working code for one version. 
If this code affects the instance-specific code, then that goes back into the Content file. 
If the change afects the common code, then that goes back into the Template file. Then the other 
Content files can be generated with the fix, verified, and deployed. 

Implementation
--------------
Template and Content files are tagged with XML.
merge.py uses xmltodict, json. and collections.
Parameters are --template, --content, and --merged. 

XML tags: 
<body></body> encloses the entire template or content file.

<sections></sections> encloses the list of sections.

<section id="sectionName"></section> encloses a named section of code. Every named section of code must exist in the template. If a section in the template must be "empty" and supplied by the content then just put a comment line in the template and supply the text in the contents. If a named section does not exist in a content, then the section is taken as-is from the template. Sections are added to a collections.OrderedDict so section order is determined by the template. 

At least two <section> tags are required in a content. I'm not going to fix this because a one-section substitution is trivial and fixing this adds unnecessary complexity. 

<commentMarker>//</commentMarker> sets the line-based comment marker. For example, in LSL or Java this would be // while in Python this would be #. 

Since the template and content files are xml, certain characters are illegal in text. You will need to make these common substitutions: 
	< becomes &lt;
	> becomes &gt;
	& becomes &amp;

The Merge process marks sections by name using the Comment marker. The source files are listed at the top of the output file, also denoted with comment markers. 

Example Files
-------------
template.xml
<body>
<commentMarker>//</commentMarker>
<sections>
<section id="section1">
code1
</section>
<section id="section2">
code2 from template
</section>
<section id="section3">
code3
</section>
</sections>
</body>

content.xml 
<body>
<template>template</template>
<sections>
<section id="section2">
// python merge.py --template template.xml --content content.xml --merged merged.txt
code2 from content
</section>
<section id="section3">
code3 from content
</section>
</sections>
</body>

The comment in the first section is a convention: make it convenient to get the complete merge command. 
It needs to go into a content section because the code doesn't look for content anywhere else. 

To merge these files, run $python merge 
or $python merge --template template.xml --content content.xml --merged merged.xml . 
or $python merge -t template.xml -c content.xml -m merged.xml . 
The result will show up in merged.txt:
// ---- merge --template template.xml --content content.xml --merged merged.txt
// ---- merge section: section1
code1 from template
// ---- merge section: section2
code2 from content
// ---- merge section: section3
code3 from content

merge.py places the complete command into the top of the merged file. 
It may also be good practice to keep that in the content file as well. 
merge.py starts its comments with // ---- merge so that an underage utility can separate a merged file back into a content file and something resembling a template file. The idea here is that if you edit a merged file, you will want to be able to extract the edits and put them into the template and content files. Changes made in the template area would then automatically propagate to the other versions. 

Planned XML Tags
----------------
<additional></additional> encloses text to be added here to the text in a <section>. 

<section>
	<substitutions>
		<substitution>
			<template>original text</template>
			<content>replacement text></content>
		</substitution>
	</substitutions>
</section>

Frequently a section of code has a handful of changes interspersed with code that's not to change. It's a pain in the butt to define a handful of <section> pairs and maintain their order. Instead, specify each substitution in a list. 

