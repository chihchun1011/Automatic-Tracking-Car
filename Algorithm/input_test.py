import student
interface = student.interface()

getchr=interface.wait_for_node()
while getchr=='0':
        getchr=interface.wait_for_node()
print("get:",getchr)
dirc=int(input("next direction: "))
interface.send_action(dirc)
while dirc !='q':
        getchr=interface.wait_for_node()
        while getchr=='0':
                getchr=interface.wait_for_node()
        print("get:",getchr)
        dirc=int(input("next direction: "))
        interface.send_action(dirc)
        
print("end testing")
