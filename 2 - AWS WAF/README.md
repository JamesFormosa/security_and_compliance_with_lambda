# Automating WAF IP List Updates with AWS Lambda

## Setup Artillery Instances
   <details>
    <summary> Adjust the default security group settings in the default vpc to allow ssh access from your ip.</summary>
    
    1. Navigate to the EC2 dashboard and click on *Security groups* under *Resources*
    2. Click the check-box next to the security group with a *Group Name* of "defualt" and open the *Inbound* tab.
    3. Click the *Edit* button and on the *Edit inbound rules* dialog box click the *Add Rule* button. 
    4. Set *Type* to "SSH", *Soure* to "My IP" and click the *Save* button.
   </details>
   * Create and download a key pair.
   * Launch the artillery instances.
2. Review the Resources Being Protected
3. Complete Setup of WAF
4. Configure Lambda Function
