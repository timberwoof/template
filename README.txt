Templating sytsem so that multiple versions of some function can exist based off a single template. 

For example, there are four Black Gazza doors with very similar functionality. 
Differences lie in things like geometry and prim and face assignments. 
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

Markers start with // ### 
// ### Template
code1
// ### Start <symbol>
// ### Stop <symbol>
code3

// ### Content
// ### Template <filename>
// ### Start <symbol>
code2
// ### Stop <symbol>

// ### Merged
// ### Template <filename>
// ### Content <filename>
code1
// ### Start <symbol>
code2
// ### Stop <symbol>
code3

Start and Stop markers must be paired, no nesting. 
The system is line-based. Markers cannot be in the middle of a line. 
The user must intelligently manage start/stop sections. 
