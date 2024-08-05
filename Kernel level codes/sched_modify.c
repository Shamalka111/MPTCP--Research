#include <linux/kernel.h>
#include <linux/netdevice.h>
#include <linux/skbuff.h>
#include <linux/tcp.h>
#include <linux/mptcp.h>

struct sock *get_available_subflow(struct sock *meta_sk, struct sk_buff *skb,
				   bool zero_wnd_test)
{
	struct mptcp_cb *mpcb = tcp_sk(meta_sk)->mpcb;
	struct sock *sk;
	bool looping = false, force;
	struct mptcp_tcp_sock *mptcp;

	/* Answer data_fin on same subflow!!! */
	if (meta_sk->sk_shutdown & RCV_SHUTDOWN && skb &&
	    mptcp_is_data_fin(skb)) {
		mptcp_for_each_sub(mpcb, mptcp)
		{
			sk = mptcp_to_sock(mptcp);

			if (tcp_sk(sk)->mptcp->path_index ==
				    mpcb->dfin_path_index &&
			    mptcp_is_available(sk, skb, zero_wnd_test)) {
				/* Print MTU of the chosen subflow */
				printk(KERN_INFO "Selected subflow MTU: %d\n",
				       dev_get_by_name(&init_net, 
				       skb->dev->name)->mtu);
				return sk;
			}
		}
	}

	/* Find the best subflow */
restart:
	sk = get_subflow_from_selectors(mpcb, skb, &subflow_is_active,
					zero_wnd_test, &force);
	if (force) {
		/* Print MTU of the chosen subflow */
		printk(KERN_INFO "Selected active subflow MTU: %d\n",
		       dev_get_by_name(&init_net, 
		       skb->dev->name)->mtu);
		return sk;
	}

	sk = get_subflow_from_selectors(mpcb, skb, &subflow_is_backup,
					zero_wnd_test, &force);
	if (!force && skb) {
		/* Print MTU of the chosen backup subflow */
		printk(KERN_INFO "Selected backup subflow MTU: %d\n",
		       dev_get_by_name(&init_net, 
		       skb->dev->name)->mtu);

		/* Clean the path mask if necessary */
		TCP_SKB_CB(skb)->path_mask = 0;

		if (!looping) {
			looping = true;
			goto restart;
		}
	}
	return sk;
}
