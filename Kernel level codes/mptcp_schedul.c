// Include necessary headers
#include <net/mptcp.h>
#include <net/tcp.h>

// Example function to get Path MTU of a subflow
static inline int get_subflow_pmtu(struct sock *sk)
{
    return sk->sk_pmtu;
}

// Modified scheduling function
void mptcp_schedule(struct sock *meta_sk, struct sk_buff *skb)
{
    struct mptcp_cb *mpcb = tcp_sk(meta_sk)->mpcb;
    struct mptcp_tcp_sock *mptcp;
    int best_pmtu = 0;
    struct sock *best_sk = NULL;

    mptcp_for_each_subflow(mpcb, mptcp)
    {
        struct sock *sk = mptcp_to_sock(mptcp);
        int pmtu = get_subflow_pmtu(sk);

        // Check if this subflow is suitable based on existing criteria
        if (!mptcp_is_active(mptcp) || sk->sk_err)
            continue;

        // Check if the packet size fits the Path MTU
        if (skb->len <= pmtu)
        {
            // Select the subflow with the highest PMTU that fits the packet
            if (pmtu > best_pmtu)
            {
                best_pmtu = pmtu;
                best_sk = sk;
            }
        }
    }

    // If a suitable subflow is found, schedule the packet on it
    if (best_sk)
    {
        tcp_transmit_skb(best_sk, skb, 1);
    }
    else
    {
        // Handle case where no suitable subflow is found
    }
}
