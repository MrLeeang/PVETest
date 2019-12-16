#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/11/26 17:39
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : test.py
# @Software     : PyCharm


from proxmoxer import ProxmoxAPI
import time
import json
import sys

proxmox = ProxmoxAPI('192.168.161.20', user='root@pam',
                     password='1Password.@integrity', verify_ssl=False)


def clone_vm():
    # for vm in proxmox.nodes('pve').qemu.get():
    #     if vm.get('template') and vm.get("name") == "centos7-tpl":

    for vm in proxmox.cluster.resources.get(type='vm'):
        if vm.get("template"):
            if vm.get("name") == "centos7-tpl":
                node = vm.get("node")
                vmid = vm.get("vmid")
                for i in range(19):
                    next_vmid = 282+i
                    task_id = proxmox.nodes(node).qemu(vmid).clone.post(name="clone-centos7-{}".format(next_vmid), newid=next_vmid)
                    print(task_id)
                    # res = proxmox.cluster.tasks.get()
                    # print(json.dumps(res))
                    while True:
                        task = proxmox.nodes(node).tasks(task_id).status.get()
                        if task.get("status", '') == "stopped" and task.get("exitstatus", '') == "OK":
                            break
                        time.sleep(2)

            # proxmox.nodes('pve').qemu(vmid).delete()
            # time.sleep(0.3)


def start_all_vm():
    for vm in proxmox.cluster.resources.get(type='vm'):
        if not vm.get("template"):
            # "stopped", "running"
            if vm.get("status", '') == "running":
                continue
            node = vm.get("node")
            vmid = vm.get("vmid")
            task_id = proxmox.nodes(node).qemu(vmid).status.start.post()
            while True:
                task = proxmox.nodes(node).tasks(task_id).status.get()
                if task.get("status", '') == "stopped" and task.get("exitstatus", '') == "OK":
                    break
                time.sleep(0.5)


def stop_all_vm():
    for vm in proxmox.cluster.resources.get(type='vm'):
        if not vm.get("template"):
            # "stopped", "running"
            if vm.get("status", '') == "stopped":
                continue
            node = vm.get("node")
            vmid = vm.get("vmid")
            task_id = proxmox.nodes(node).qemu(vmid).status.stop.post()
            while True:
                task = proxmox.nodes(node).tasks(task_id).status.get()
                if task.get("status", '') == "stopped" and task.get("exitstatus", '') == "OK":
                    break
                time.sleep(0.5)


def get_vnc_console():
    for vm in proxmox.cluster.resources.get(type='vm'):
        if not vm.get("template"):
            # "stopped", "running"
            if vm.get("status", '') == "stopped":
                continue
            if vm.get("name") != "clone-centos7-113":
                continue
            node = vm.get("node")
            vmid = vm.get("vmid")
            vncproxy = proxmox.nodes(node).qemu(vmid).vncproxy.post()
            vncticket = vncproxy.get("ticket")
            port = vncproxy.get("port")
            return json.dumps({"port": port, "vncticket": vncticket})


if __name__ == "__main__":
    # clone_vm()
    start_all_vm()
    # stop_all_vm()
    # get_vnc_console()
    # for i in proxmox.cluster.resources.get(type='vm'):
    #     print(i)
    #     exit()
    pass
