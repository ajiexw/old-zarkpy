#!/usr/bin/env python
#coding=utf-8
import sphinxapi

host = 'aoaola_search'
port = 9312

def search(**argvs):
    argvs.setdefault('query', '')
    argvs.setdefault('mode', sphinxapi.SPH_MATCH_ALL)
    argvs.setdefault('index', '*')

    cl = sphinxapi.SphinxClient()
    cl.SetServer ( host, port )
    cl.SetWeights ( [100, 1] )
    cl.SetMatchMode ( argvs['mode'] )

    if argvs.has_key('filtervals'):
        for k,v in argvs.get('filtervals'):
            cl.SetFilter(k, v)

    if argvs.has_key('groupby'):
        argvs.setdefault('groupsort', '')
        cl.SetGroupBy ( argvs['groupby'], sphinxapi.SPH_GROUPBY_ATTR, argvs['groupsort'] )
    if argvs.has_key('sortby'):
        cl.SetSortMode ( sphinxapi.SPH_SORT_EXTENDED, argvs['sortby'] )
    if argvs.has_key('limit'):
        cl.SetLimits ( int(argvs.get('start', 0)), argvs['limit'], max(argvs['limit'],1000) )
    else:
        pass
        #cl.SetLimits(0, 1000)
    res = cl.Query ( argvs['query'], argvs['index'] )

    if argvs.get('debug') and (not res):
        print 'query failed: %s' % cl.GetLastError()
        return []

    ids = [match['id'] for match in res['matches']] if res and res.has_key('matches') else []
    return ids

if __name__=='__main__':
    print search(query='粉底液', index='makeup_fine',  limit=30, debug=True, )

